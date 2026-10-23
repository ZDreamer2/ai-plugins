# Database Query Interface

## Comprehensive Example

```php
use Carbon\Carbon;

// Basic queries with different return types
$userList = Db()->list("SELECT id AS ARRAY_KEY, name, email FROM users WHERE status = ?", 'active');
// Returns: [123 => ['name' => 'John', 'email' => 'john@example.com'], ...]

$userRow = Db()->row("SELECT * FROM users WHERE id = ?", 123);  // Single row or null
$userName = Db()->cell("SELECT name FROM users WHERE id = ?", 123);  // Single value or null
$userIds = Db()->column("SELECT id FROM users WHERE role = ?", 'admin');  // [1, 2, 3]

// Named placeholders for complex queries (useful for repeated values)
$results = Db()->list("
	SELECT
		orders.id AS ARRAY_KEY,
		orders.id,
		orders.total,
		orders.created_at
	FROM orders
	JOIN users ON (users.id = orders.user_id)
	WHERE
		orders.user_id = :userId AND
		orders.created_at > :date AND
		orders.status IN (:statuses)
	ORDER BY orders.created_at DESC
	LIMIT 50
", [
	'userId' => 123,
	'date' => Carbon::now()->subMonth(),  // Automatically formatted for SQL
	'statuses' => ['pending', 'processing']  // Arrays work in IN() clauses, empty arrays too
]);

// Different database connections
$metaData = Db(Db::META)->list("SELECT * FROM configurations");  // META database
$slaveData = Db(Db::SLAVE)->list("SELECT * FROM reports");  // Read replica

// Transactions with proper error handling
try {
	Db()->beginTransaction();
	
	// Update with WHERE conditions
	Db()->update(
		table: 'users',
		data: ['last_login' => Carbon::now()],
		id: 123  // Shorthand for ['id' => 123]
	);
	
	// Insert and get generated ID
	Db()->insert(
		table: 'logs',
		data: [
			'user_id' => 123,
			'action' => 'login',
			'created_at' => Db()->now()  // NOW() function
		]
	);
	$logId = Db()->lastId();
	
	Db()->commit();
} catch (Exception $e) {
	Db()->rollback();
	throw $e;
}

// Batch operations and special insert modes
Db()->insertBatch(
	table: 'products',
	data: [
		['name' => 'Product 1', 'price' => 100],
		['name' => 'Product 2', 'price' => 200],
	]
);

Db()->insert(
	table: 'settings',
	data: ['key' => 'theme', 'value' => 'dark'],
	operation: 'REPLACE'  // Also supports INSERT IGNORE
);

// Get generated SQL without executing (useful for dynamic fragments in larger queries)
$likeSql = Db()->sql("name LIKE ?", "%search%");
// Returns: "name LIKE '%search%'"
```

## Rules

- NEVER mix Db() and old Bc_Db in same transaction (separate connection pools)
- ALWAYS use placeholders for user input (? or :name)
- MUST handle empty arrays in IN() clauses - they work correctly
- ARRAY_KEY column alias becomes array keys in list() and column() results

## Additional Patterns

### Complex WHERE Conditions

```php
// Update with multiple conditions
Db()->update(
	table: 'orders',
	data: ['status' => OrderStatus::COMPLETED],  // Enums work
	where: [
		'user_id' => $userId,
		'status' => ['pending', 'processing']  // Arrays for IN()
	]
);

// Named placeholders when value is repeated
$data = Db()->list("
	SELECT * FROM orders
	WHERE created_by = :userId OR assigned_to = :userId
", ['userId' => $currentUser]);
```

### Working with Different Databases

```php
// Specific databases beyond newbicotender
$redmineData = Db(Db::REDMINE)->list("SELECT * FROM issues");
$searchResults = Db(Db::MANTICORE)->list("SELECT * FROM products_index");
```

### SQL Formatting

Each major clause (SELECT, FROM, JOIN, WHERE, GROUP BY, ORDER BY, LIMIT) starts on its own line:

```php
$data = Db()->list("
	SELECT
		payment.payment_id,
		payment.date AS payment_date,
		bill.cost AS bill_cost
	FROM payment
	JOIN bill ON (payment.bill_id = bill.bill_id)
	LEFT JOIN manager ON (bill.manager_id = manager.manager_id)
	WHERE
		bill.status = 'bill' AND
		bill.isVoid = 0 AND
		payment.date BETWEEN :from AND :to
	ORDER BY payment.date DESC
	LIMIT 20
", ['from' => $from, 'to' => $to]);
```

- SELECT columns can be on one line or one-per-line as readability demands
- WHERE can be on one line when short: `WHERE user_id = ?`
- Multi-line WHERE: each condition on its own line, AND/OR at end of line
- JOIN ON conditions in parentheses: `JOIN bill ON (payment.bill_id = bill.bill_id)`
- Use full table names, not aliases — `time_entries.user_id` not `te.user_id`. Aliases are like `$i` variables: they force a mental mapping. Allow aliases only when structurally required (self-joins, subqueries referencing outer table).

### Placeholder Conversions

- null -> NULL
- bool -> 1 or 0
- DateTime/Carbon -> 'Y-m-d H:i:s'
- BackedEnum -> its value
- UnitEnum -> its name
- Ulid -> hex representation
- array -> comma-separated values (empty -> NULL, no nesting)