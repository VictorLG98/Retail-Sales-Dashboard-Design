import reflex as rx
from app.state import DashboardState


def kpi_card(kpi: dict) -> rx.Component:
    """A card component to display a Key Performance Indicator."""
    return rx.el.div(
        rx.el.div(
            rx.el.p(kpi["title"], class_name="text-sm font-medium text-gray-500"),
            rx.el.p(kpi["value"], class_name="text-3xl font-bold text-gray-900 mt-1"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.cond(
                kpi["change_type"] == "increase",
                rx.icon("arrow-up", class_name="h-5 w-5 text-green-500"),
                rx.icon("arrow-down", class_name="h-5 w-5 text-red-500"),
            ),
            rx.el.span(
                kpi["change"],
                class_name=rx.cond(
                    kpi["change_type"] == "increase",
                    "text-green-600 font-semibold",
                    "text-red-600 font-semibold",
                ),
            ),
            class_name="flex items-center gap-1 text-sm mt-2",
        ),
        class_name="bg-white rounded-2xl p-6 flex flex-col shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:shadow-[0px_4px_8px_rgba(0,0,0,0.15)] transition-shadow duration-300",
    )


def nav_item(item: dict, collapsed: rx.Var[bool]) -> rx.Component:
    """A navigation item for the sidebar."""
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5 shrink-0"),
        rx.cond(collapsed, None, rx.el.span(item["label"], class_name="truncate")),
        href=item.get("href", "#"),
        class_name="flex items-center gap-3 px-4 py-2.5 rounded-lg text-gray-700 hover:bg-sky-100 hover:text-sky-700 transition-colors duration-200",
    )


def sidebar() -> rx.Component:
    """The sidebar component for navigation."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("store", class_name="h-8 w-8 text-sky-600"),
                rx.cond(
                    DashboardState.sidebar_collapsed,
                    None,
                    rx.el.span(
                        "RetailCo", class_name="text-xl font-bold text-gray-800"
                    ),
                ),
                class_name="flex items-center gap-3 h-16 px-4 border-b border-gray-200",
            ),
            rx.el.nav(
                rx.foreach(
                    DashboardState.sidebar_items,
                    lambda item: nav_item(item, DashboardState.sidebar_collapsed),
                ),
                class_name="flex-1 overflow-auto p-4 space-y-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        rx.cond(
                            DashboardState.sidebar_collapsed,
                            "chevrons-right",
                            "chevrons-left",
                        ),
                        class_name="h-5 w-5",
                    ),
                    on_click=DashboardState.toggle_sidebar,
                    class_name="p-2 rounded-lg text-gray-600 hover:bg-gray-200",
                ),
                class_name="border-t border-gray-200 p-4 flex justify-center",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=rx.cond(
            DashboardState.sidebar_collapsed,
            "w-20 bg-white border-r border-gray-200 transition-all duration-300 ease-in-out",
            "w-64 bg-white border-r border-gray-200 transition-all duration-300 ease-in-out",
        ),
    )


def header() -> rx.Component:
    """The main header of the dashboard content."""
    return rx.el.header(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-3xl font-bold text-gray-900"),
            rx.el.p(
                "Welcome back, here's your sales overview.",
                class_name="text-gray-500 mt-1",
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Export Data",
                rx.icon("download", class_name="ml-2 h-4 w-4"),
                class_name="bg-sky-600 text-white px-4 py-2 rounded-lg text-sm font-semibold flex items-center shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:bg-sky-700 transition-colors duration-300",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center pb-6 border-b border-gray-200",
    )


def time_granularity_toggle() -> rx.Component:
    """A segmented control to switch time granularity."""
    options = ["Daily", "Weekly", "Monthly"]
    return rx.el.div(
        rx.foreach(
            options,
            lambda option: rx.el.button(
                option,
                on_click=lambda: DashboardState.set_time_granularity(option),
                class_name=rx.cond(
                    DashboardState.time_granularity == option,
                    "px-3 py-1.5 text-sm font-semibold text-white bg-sky-600 rounded-lg shadow-sm",
                    "px-3 py-1.5 text-sm font-semibold text-gray-600 bg-white hover:bg-gray-100 rounded-lg",
                ),
            ),
        ),
        class_name="flex items-center p-1 space-x-1 bg-gray-100 rounded-lg",
    )


def sales_chart() -> rx.Component:
    """The sales trend line chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Sales Trends", class_name="text-lg font-semibold text-gray-900"
                ),
                rx.el.p(
                    "An overview of your sales performance.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            time_granularity_toggle(),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", vertical=False, stroke="#e5e7eb"
            ),
            rx.recharts.graphing_tooltip(
                cursor={"stroke": "#d1d5db", "strokeWidth": 1}
            ),
            rx.recharts.x_axis(
                data_key="name",
                tick_line=False,
                axis_line=False,
                stroke="#6b7280",
                font_size=12,
            ),
            rx.recharts.y_axis(
                tick_line=False, axis_line=False, stroke="#6b7280", font_size=12
            ),
            rx.recharts.line(
                data_key="sales",
                stroke="#0284c7",
                stroke_width=2,
                dot=False,
                type_="monotone",
            ),
            data=DashboardState.sales_data,
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
            class_name="[&_.recharts-tooltip-item-unit]:text-gray-600 [&_.recharts-tooltip-item-value]:!text-gray-900 [&_.recharts-tooltip-wrapper]:z-[1]",
        ),
        class_name="bg-white rounded-2xl p-6 shadow-[0px_1px_3px_rgba(0,0,0,0.12)]",
    )


def filters() -> rx.Component:
    """Component containing all filter controls."""
    return rx.el.div(
        rx.el.h3("Filters", class_name="text-lg font-semibold text-gray-900 mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Store Location",
                    class_name="text-sm font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.foreach(
                        DashboardState.store_locations,
                        lambda location: rx.el.option(location, value=location),
                    ),
                    placeholder="Select a store",
                    on_change=DashboardState.set_selected_store,
                    class_name="w-full p-2 border border-gray-300 rounded-lg text-sm",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.label(
                    "Product Category",
                    class_name="text-sm font-medium text-gray-700 mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        DashboardState.product_categories,
                        lambda category: rx.el.div(
                            rx.el.input(
                                type="checkbox",
                                id=category.lower(),
                                on_change=lambda _: DashboardState.toggle_category(
                                    category
                                ),
                                class_name="h-4 w-4 rounded border-gray-300 text-sky-600 focus:ring-sky-500",
                            ),
                            rx.el.label(
                                category,
                                htmlFor=category.lower(),
                                class_name="ml-2 text-sm text-gray-600",
                            ),
                            class_name="flex items-center",
                        ),
                    ),
                    class_name="space-y-2",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.label(
                    "Date Range", class_name="text-sm font-medium text-gray-700 mb-1"
                ),
                rx.el.div(
                    rx.el.input(
                        type="date",
                        on_change=DashboardState.set_start_date,
                        class_name="w-full p-2 border border-gray-300 rounded-lg text-sm",
                    ),
                    rx.el.input(
                        type="date",
                        on_change=DashboardState.set_end_date,
                        class_name="w-full p-2 border border-gray-300 rounded-lg text-sm",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="w-full",
            ),
            class_name="space-y-4",
        ),
        class_name="bg-white rounded-2xl p-6 shadow-[0px_1px_3px_rgba(0,0,0,0.12)] h-fit",
    )


def main_content() -> rx.Component:
    """The main content area of the dashboard."""
    return rx.el.main(
        header(),
        rx.el.div(
            rx.foreach(DashboardState.kpi_data, kpi_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6",
        ),
        rx.el.div(
            rx.el.div(sales_chart(), class_name="lg:col-span-2"),
            filters(),
            class_name="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        rx.el.div(top_products_table(), class_name="mt-8"),
        class_name="flex-1 p-6 overflow-y-auto",
    )


def table_header(name: str, key: str) -> rx.Component:
    """A sortable table header cell."""
    return rx.el.th(
        rx.el.div(
            name,
            rx.cond(
                DashboardState.sort_by == key,
                rx.icon(
                    rx.cond(
                        DashboardState.sort_order == "desc", "arrow-down", "arrow-up"
                    ),
                    class_name="h-4 w-4 ml-1",
                ),
                rx.el.div(class_name="h-4 w-4 ml-1"),
            ),
            class_name="flex items-center",
        ),
        on_click=lambda: DashboardState.set_sorting(key),
        class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider cursor-pointer select-none hover:bg-gray-100",
        scope="col",
    )


def top_products_table() -> rx.Component:
    """The data table for top-selling products."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Top Products", class_name="text-lg font-semibold text-gray-900"
                ),
                rx.el.p(
                    "Best-selling items in the current selection.",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search products...",
                    on_change=DashboardState.set_product_search_query.debounce(300),
                    class_name="w-full max-w-sm pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-sky-500 focus:border-sky-500",
                ),
                class_name="relative",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        table_header("Product Name", "name"),
                        table_header("Units Sold", "units_sold"),
                        table_header("Total Revenue", "total_revenue"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.filtered_and_sorted_products,
                        lambda product: rx.el.tr(
                            rx.el.td(
                                product["name"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(
                                product["units_sold"].to_string(),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            rx.el.td(
                                rx.el.span(f"${product['total_revenue']:.2f}"),
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
                            ),
                            class_name="border-b border-gray-200 hover:bg-gray-50",
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-hidden border-b border-gray-200 rounded-2xl shadow-[0px_1px_3px_rgba(0,0,0,0.12)]",
        ),
        class_name="bg-white p-6 rounded-2xl",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        main_content(),
        class_name="flex h-screen w-full bg-gray-50 font-['Raleway']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)