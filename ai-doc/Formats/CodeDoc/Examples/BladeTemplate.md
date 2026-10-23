# Blade Templates - Laravel Templating for BicoTender

## Comprehensive Example

```blade
@use('Bc\Modules\Shop\Widgets\ProductList\ProductListWidget')
@php /** @var ProductListWidget $widget */ @endphp

<div {{$widget->live->tagId($widget::PANEL_MAIN)}}>
	<h1>{{ $widget->title }}</h1>

	@foreach($widget->products as $product)
		{{ $widget->view('productCard', ['product' => $product, 'showPrice' => true]) }}
	@endforeach

	@if($widget->hasMorePages)
		<button>Load more</button>
	@endif

	<div @class([
		'summary',
		'empty' => $widget->products->isEmpty(),
	])>
		Total: {{ $widget->products->count() }}
	</div>
</div>
```

## Tooltips

`MessageList` renders tooltips via `data-tooltip` attribute. Two patterns:

```blade
{{-- Static text or array of lines --}}
<button {{ MessageList::tooltip('Simple text tooltip') }}>Hover me</button>
<span {{ MessageList::tooltip(['Line one', 'Line two']) }}>Multi-line</span>

{{-- Objects with ->tooltip() returning MessageList (Htmlable, renders via {{ }}) --}}
<span {{ $issue->priority->tooltip() }}>{{ $issue->priority->icon() }}</span>
```

Tooltips support HTML formatting and interactive links.

## Rules

- MUST use tabs for indentation in `.blade.php` files
- MUST use `@class` directive for non-trivial conditional class lists
- MUST add `@use` directive at top for all classes used in the template
- MUST NOT use inline styles or Tailwind classes - CSS is added separately
- NEVER use inline ternary operators for complex class logic
