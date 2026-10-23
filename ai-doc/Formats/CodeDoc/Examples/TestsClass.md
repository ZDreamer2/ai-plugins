# Writing Tests

PHPUnit tests using real system components with automatic rollback. Tests are structured as scenarios: set up conditions, execute a sequence of operations with assertions at each step, verify final state.

## Testing Philosophy

Tests use real systems with automatic rollback. Database, sessions, logging, and caching work exactly like production.

- Real database: Identical structure to production, automatic rollback after each test
- No mocks needed: Sessions, logging, repositories work normally
- Just works: `$this->loginManager()`, `$this->assertLogs()` - no configuration
- Mock only external APIs: Use real systems for internal components

This approach catches real integration issues while keeping tests simple.

## Comprehensive Example

```php
// src/Modules/Reports/Core/Tests/ReportManagerTest.php
class ReportManagerTest extends ReportTestAbstract {
	public function testProcessAndPublishWorkflow() {
		// ARRANGE — analyst with a new report
		$this->loginManager(ManagerSeeder::ANALYST);
		$report = $this->createReport();

		$manager = $this->reportManager($report);

		// Process — collects data, transitions to completed
		$manager->process();
		$this->assertDump(ReportStatus::COMPLETED, $this->getReport($report->id)->status);
		$this->assertLogs("
			12:00:00: Report[{$report->id}] Processing started
			12:00:00: Report[{$report->id}] Data collected: 150 records
			12:00:00: Report[{$report->id}] Processing completed
		");

		// Re-process — idempotent, no state change
		$manager->process();
		$this->assertLogs("
			12:00:00: Report[{$report->id}] Already processed, skipping
		");

		// Publish — transitions to published, creates notification
		$manager->publish();
		$this->assertDump(ReportStatus::PUBLISHED, $this->getReport($report->id)->status);

		// Verify final state: complete audit trail
		$this->assertDump([
			['action' => 'process', 'actor' => ManagerSeeder::ANALYST],
			['action' => 'publish', 'actor' => ManagerSeeder::ANALYST],
		], $this->getAuditRows($report->id));
	}
}
```

A scenario test is ARRANGE followed by sequential ACT-ASSERT steps. ARRANGE starts with a comment summarizing what was set up and why. Each step has an inline comment narrating what happens.

A simple behavior needing only one operation is just a single-step scenario — no special treatment needed.

## Abstract Test Base

When tests share domain setup (session config, seeded data helpers, DB readers), extract into an abstract class in `Support/`:

```php
// src/Modules/Reports/Core/Tests/Support/ReportTestAbstract.php
abstract class ReportTestAbstract extends MyTestCase {
	protected function createReport(): Report { ... }
	protected function getReport(int $id): Report { ... }
	protected function reportManager(Report $report): ReportManager { ... }
	protected function getAuditRows(int $reportId): array { ... }
}
```

Helpers reduce noise in tests — domain setup, state readers, expected result factories, whatever is repeated across test methods.

## Assertions

Use `assertDump` for arrays, objects, and structured data. Use `assertEquals` for strings and simple values.

ALWAYS use ONE `assertDump` to check entire arrays/objects — NEVER check individual fields separately:

```php
// CORRECT: single assertDump verifies complete structure
$this->assertDump([
	'status' => 'ok',
	'username' => 'john',
], $data);

// INCORRECT: wastes assertions, misses unexpected fields
// $this->assertDump('ok', $data['status']);
// $this->assertDump('john', $data['username']);
```

When structure contains entities not relevant to the test, convert to named ghosts:

```php
$this->assertDump($expected, $actual, toGhost: [WorkIssue::class, WorkActor::class]);
```

`assertDump` compares constructor parameters only — private properties set after construction (like back-references) are excluded from comparison. Works with nested Value Objects:

```php
// assertDump with nested VOs — compares constructor parameters recursively
$this->assertDump(new NamedIdsTableThead([
	new NamedIdsTableTheadTr([
		new NamedIdsTableTheadTh(colSpan: 2, rowSpan: 1, id: 1),
		new NamedIdsTableTheadTh(colSpan: 1, rowSpan: 1, id: 2),
	]),
]), $tableHead->getTableHead());
```

Use heredoc syntax for multiline strings:

```php
$expected = <<<EOF
Line 1
Line 2
Line 3
EOF;
$this->assertEquals($expected, $result);
```

## Test Location

Place tests in a `Tests/` subdirectory within the unit being tested:
- `src/Domain/Manager/Manager/Tests/ManagerTest.php`
- `src/Modules/ProjectManagement/Domain/RmUser/Tests/RmUserTest.php`

Many existing tests are in the `/tests` directory (legacy location).

## Rules

- MUST extend from `MyTestCase` directly or indirectly
- MUST use ONE `assertDump` to check entire arrays/objects — NEVER check individual fields separately
- MUST use heredoc syntax (<<<EOF) for multiline strings — NEVER concatenate with "\n"
- MUST use `assertEquals` for strings and simple values, `assertDump` for structured data
- SHOULD structure tests as scenarios with sequential ACT-ASSERT steps sharing one ARRANGE
- SHOULD start ARRANGE with a comment summarizing what was set up and why
- SHOULD combine related behaviors sharing costly setup into one scenario test
- SHOULD avoid using `setUp` method
- ALWAYS run tests after changes through `./app test`
- ALWAYS create support classes in a `Support` directory adjacent to the test file

## Additional Documentation

* `src/Core/Domain/Tests/EntityTest/Docs/BuildEntityTest.md` - Read when writing Entity tests
* `src/Core/Widget/LiveWidget/Docs/LiveWidgetTests.md` - Read when writing LiveWidget tests
* `src/Core/Tests/Docs/WorkingWithDb.md` - Read when testing database operations
* `src/Core/Tests/Docs/ApiServiceTests.md` - Read when testing code that calls external APIs
* `src/Core/Tests/Docs/FullActionTests.md` - Read when testing HTTP actions end-to-end (request dispatch, response assertions)
