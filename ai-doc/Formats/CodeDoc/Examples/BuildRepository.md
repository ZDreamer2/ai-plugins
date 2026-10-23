# Repository - Entity Persistence Handler

## MUST read to understand Repository

- @src/Core/Domain/Docs/EntityOverview.md - Understand Entity-Repository-Collection triad before implementing
- @src/Core/Domain/Docs/BuildEntityUnit.md - Consider related files that may need updates (tests, seeders) when editing Repository
- `{EntityPath}/Docs/UnitGuide.md` - Apply business requirements for the specific Entity being implemented

## Comprehensive Example

```php
<?php
namespace Bc\Modules\Analytics\Domain\Report\Report;

use Bc\Configuration\Pdo\Types\PdoSchema;use Bc\Core\Domain\Repository\Repository;use Bc\Core\Domain\Repository\Types\DeleteStrategy;use Bc\Core\Domain\Repository\Types\Plugin\ChildEntityLink;use Bc\Core\Domain\Repository\Types\Plugin\ParentEntityLink;use Bc\Core\Domain\Repository\Types\Plugin\UserLink;use Bc\Core\Domain\Repository\Types\RepositoryOptions;

/**
 * @extends Repository<Report, ReportCollection>  // MUST specify Entity and Collection types
 */
class ReportRepository extends Repository {
	public static function getOptions(): RepositoryOptions {
		return new RepositoryOptions(
			schema: PdoSchema::ANALYTICS,           // Database schema (enum)
			table: 'report',                        // Table name
			deleteStrategy: DeleteStrategy::DELETED_AT,  // Soft delete via deletedAt field
			isEditable: true,                       // Can save/delete (false for read-only)
		);
	}

	public static function buildLinks(): array {
		return [
			// Field name => Link plugin configuration
			'schema' => new ParentEntityLink(),     // Required parent entity
			'author' => new UserLink(),             // Special user reference handling
			'currentRun' => new ChildEntityLink(),  // Single child entity
		];
	}

	protected function init(): void {
		$this->initPluginsAndEvents();  // MUST call if buildLinks() is defined
	}

	// Event handlers: protected onXxxEvent methods are auto-registered
	// Alternative: $this->events->on(EventClass::class, $callable) for manual registration
}
```

## Repository Options

Configure how Repository interacts with database:

```php
new RepositoryOptions(
	schema: PdoSchema::BICO,              // Default schema
	table: 'my_table',                    // Required table name
	deleteStrategy: DeleteStrategy::NONE,  // No soft delete
	isEditable: false,                    // Read-only repository
	defaultOrderBy: ['spent_on DESC'],    // Default ORDER BY, overridable via GetListOptions::orderBy
)
```

Available delete strategies:
- `DeleteStrategy::NONE` - Hard delete (permanent removal)
- `DeleteStrategy::DELETED_AT` - Soft delete via deletedAt timestamp
- `DeleteStrategy::IS_DELETED` - Soft delete via is_deleted boolean flag

## Plugins

Repository plugins extend functionality without custom code.

### Quick Plugin Selection

| Plugin | Use When | Docs |
|--------|----------|------|
| **Simple Plugins** |||
| `HistorySaver` | Need audit trail for field changes | `src/Core/Domain/Repository/Docs/Build/Plugins/HistorySaver.md` |
| **Entity Link Plugins** (all use EntityLinkPlugin) |||
| `ParentEntityLink` | Entity MUST belong to another (non-null) | `src/Core/Domain/Repository/Docs/Build/Plugins/EntityLink.md` |
| `AssociatedEntityLink` | Optional reference to independent entity | `src/Core/Domain/Repository/Docs/Build/Plugins/EntityLink.md` |
| `ChildEntityLink` | Entity owns single child | `src/Core/Domain/Repository/Docs/Build/Plugins/EntityLink.md` |
| **Collection Plugin** |||
| `ChildrenCollectionLink` | Entity owns multiple children | `src/Core/Domain/Repository/Docs/Build/Plugins/ChildrenCollectionLink.md` |
| **User Plugin** |||
| `UserLink` | Reference to User with type support | `src/Core/Domain/Repository/Docs/Build/Plugins/UserLink.md` |

**IMPORTANT**: Always read the plugin documentation file before using any plugin. Each plugin has specific parameters, behaviors, and usage patterns that MUST be understood for correct implementation.

## Rules

- MUST extend `Bc\Core\Domain\Repository\Repository` base class
- MUST implement `getOptions()` method returning `RepositoryOptions`
- MUST specify Entity and Collection types via PHPDoc `@extends`
- MUST call `initPluginsAndEvents()` in `init()` if `buildLinks()` returns links
- ALWAYS match link field names to Entity property names

## Custom Filtering

For virtual filter aliases (e.g., `'saleManagers' => 1` → `'managerId' => [4, 13, 45]`), see `src/Core/Domain/Repository/Docs/Build/CustomFiltering.md`.

## Event System

Repositories have a low-level event system for advanced customization. Link plugins handle most common cases automatically.

Two ways to register event handlers:
1. **Auto-registration**: define `protected` method named `onXxxEvent` - registered automatically by `initPluginsAndEvents()`
2. **Manual**: call `$this->events->on(EventClass::class, $callable)` - use when registering from other classes, before plugins, or with custom callables

Available events:
- `PreSaveEvent` - Before entity validation
- `RowPreSaveEvent` - Before database insert/update
- `RowSavedEvent` - After database save
- `RetrieveQueryPreBuildEvent` - Modify SELECT query
- `FilterConditionRebuildEvent` - Transform custom filter conditions
- `RowsRetrievedEvent` - Process retrieved data

For advanced event usage, see `src/Core/Domain/Repository/Docs/Build/UsingEvents.md`.