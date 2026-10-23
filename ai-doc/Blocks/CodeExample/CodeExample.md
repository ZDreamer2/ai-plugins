# Code Example Block Format

## Basic Example

```php
namespace Tests\Core\Utils\Array\NamedIdsTableHead;

use Bc\Core\PHPUnit\MyTestCase;
use Bc\Core\Utils\Array\NamedIdsTableHead\NamedIdsTableHead;

// All tests MUST extend from MyTestCase
class NamedIdsTableHeadTest extends MyTestCase {
	public function testGetTableHead() {
		// Keep input data close to assertions for easy comparison
		$tree = new NamedIdsTree([
			['id' => 1],
			['id' => 11, 'parent' => 1],
			['id' => 2],
		]);
		$tableHead = new NamedIdsTableHead($tree);

		// MUST use ONE assertDumps to check entire structure
		$this->assertDump([
			['id' => 1, 'colSpan' => 1],
			['id' => 2, 'colSpan' => 1],
		], $tableHead->getTableHead());

		// WRONG: Multiple assertions for individual fields instead of complete structure
		// $this->assertDump(1, $thead->rows[0]->id);
		// $this->assertDump(1, $thead->rows[1]->id);
	}
}
```

## Rules

- MUST make examples dense - pack multiple teaching points into minimal code
- MUST make examples concise - show only what's necessary to demonstrate the concept
- MUST make examples self-sufficient - include enough context to understand without external references
- MUST use inline comments to explain non-obvious elements
- SHOULD add inline anti-patterns (WRONG comments) only when User explicitly mentions specific mistakes to illustrate
- MAY simplify code if it clarifies the teaching point without losing essential context