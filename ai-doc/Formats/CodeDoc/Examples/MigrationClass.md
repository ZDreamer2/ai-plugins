# Migration - Database Schema Changes

System for implementing manual database schema changes through PHP classes. Migrations auto-execute on developer machines when pages are opened, never run on production.

## Comprehensive Example

```php
namespace Bc\Configuration\Migrations;

use Bc\Configuration\Pdo\Types\PdoSchema;
use Bc\Core\Database\Migrations\Migration;
use Bc\Modules\Order\Domain\OrderStatus;

// Naming: Migration{YYYYMMDD}_{Description} - date prefix ensures execution order
class Migration20250812_EnhanceOrderSystem extends Migration {
	// Specify schema when not using default PdoSchema::BICO
	protected PdoSchema $schema = PdoSchema::ANALYTICS;

	public function up(): void {
		// ADD COLUMN: hasColumn() check ensures idempotency
		if (!$this->hasColumn('orders', 'priority')) {
			$this->db->query("
				ALTER TABLE orders
				ADD COLUMN priority TINYINT UNSIGNED NOT NULL DEFAULT 0
				AFTER status
			");
		}

		// MODIFY COLUMN: Inherently idempotent, no check needed
		$this->db->query("
			ALTER TABLE orders
			MODIFY COLUMN notes TEXT NULL DEFAULT NULL
		");

		// CREATE INDEX: hasIndex() check prevents duplicate index errors
		if (!$this->hasIndex('orders', 'idx_priority')) {
			$this->db->query("CREATE INDEX idx_priority ON orders(priority DESC)");
		}

		// CREATE TABLE: IF NOT EXISTS for idempotency
		// enumToSql() converts PHP enum to SQL ENUM('value1', 'value2', ...)
		$statusEnum = $this->enumToSql(OrderStatus::class);

		$this->db->query("
			CREATE TABLE IF NOT EXISTS orderAuditLog (
				id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
				orderId INT UNSIGNED NOT NULL,
				status $statusEnum NOT NULL,
				createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
				updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
				INDEX idx_order (orderId)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
		");
	}
}
```

## Migration Execution

### Automatic Discovery and Execution

MigrationRunner handles automatic execution:
- Location: All migrations MUST be in `src/Configuration/Migrations/`
- Naming: MUST follow pattern `Migration*.php`
- Discovery: Files discovered using Symfony Finder, sorted alphabetically
- Execution order: Alphabetical by filename (use date prefix: `YYYYMMDD`)
- Trigger: Runs when file modification time changes in migrations directory

### When Migrations Run

IMPORTANT: Migrations execute ONLY on developer machines:
- Auto-runs when opening any page via `./app page {url}`
- Triggered by MigrationRunner checking file modification times
- NEVER runs on production (checked via `Env::i()->isDev()`)
- Each migration `up()` method executes in sequence

### Idempotency

CRITICAL: All migrations MUST be idempotent - safe to run multiple times. The comprehensive example demonstrates all idempotency patterns: `hasColumn()` for columns, `hasIndex()` for indexes, `IF NOT EXISTS` for tables, and direct execution for inherently idempotent operations like MODIFY COLUMN.

## Schema Selection

Set `$schema` property to target a specific database (see comprehensive example). Available schemas from `src/Configuration/Pdo/Types/PdoSchema.php`:
- `PdoSchema::BICO` - main application schema (default)
- `PdoSchema::ANALYTICS` - analytics data
- `PdoSchema::SEO` - SEO-related tables
- `PdoSchema::CONTRACTOR` - contractor data
- `PdoSchema::SHARED` - shared data
- And others (HIRING, META, IMAP, YANDEX_METRIC, REDMINE)

Each schema maps to appropriate database profile via `pdoProfile()` method.

## Type Mapping

PHP to MySQL type mapping for migration columns:

- int -> INT (UNSIGNED for IDs/counts)
- string -> VARCHAR(255), TEXT, or LONGTEXT by length
- bool -> TINYINT(1)
- float -> DECIMAL(10,2) for money, FLOAT otherwise
- Carbon -> DATETIME
- array -> LONGTEXT (stored as JSON, default '{}' or '[]')
- PHP Enum -> ENUM(...) via enumToSql() helper

## Helper Methods

All helpers demonstrated in comprehensive example.

- `hasColumn(table, column)` - Checks column existence via `information_schema.columns`. Supports schema-qualified table names like `analytics.reports`.
- `hasIndex(table, indexName)` - Checks index existence via `information_schema.statistics`.
- `enumToSql(EnumClass::class)` - Converts PHP enum to SQL ENUM definition.

## Rules

- MUST place migrations in `src/Configuration/Migrations/` directory
- MUST name with date prefix: `Migration{YYYYMMDD}_{Description}.php`
- MUST extend `Bc\Core\Database\Migrations\Migration` class
- MUST implement `up()` method containing SQL to execute
- MUST ensure migrations are idempotent using helper methods or `IF NOT EXISTS`
- SHOULD specify `$schema` property when working with non-BICO schemas
- NEVER runs on production - development environments only
- Each migration runs every time files are modified (relies on idempotency)
