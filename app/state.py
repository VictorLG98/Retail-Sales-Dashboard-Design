import reflex as rx
from typing import TypedDict


class KpiData(TypedDict):
    title: str
    value: str
    change: str
    change_type: str


class SalesData(TypedDict):
    name: str
    sales: int


class ProductData(TypedDict):
    id: int
    name: str
    units_sold: int
    total_revenue: float


class DashboardState(rx.State):
    """The state for the retail sales dashboard."""

    kpi_data: list[KpiData] = [
        {
            "title": "Today's Revenue",
            "value": "$405,345",
            "change": "+2.5%",
            "change_type": "increase",
        },
        {
            "title": "YoY Growth",
            "value": "12.8%",
            "change": "+1.2%",
            "change_type": "increase",
        },
        {
            "title": "Avg. Transaction Value",
            "value": "$124.50",
            "change": "-$2.30",
            "change_type": "decrease",
        },
    ]
    sidebar_items: list[dict[str, str]] = [
        {"icon": "layout-dashboard", "label": "Dashboard", "href": "/"},
        {"icon": "bar-chart-3", "label": "Analytics", "href": "#"},
        {"icon": "shopping-bag", "label": "Products", "href": "#"},
        {"icon": "users", "label": "Customers", "href": "#"},
        {"icon": "settings", "label": "Settings", "href": "#"},
    ]
    sidebar_collapsed: bool = False
    time_granularity: str = "Monthly"
    sales_data: list[SalesData] = [
        {"name": "Jan", "sales": 4000},
        {"name": "Feb", "sales": 3000},
        {"name": "Mar", "sales": 2000},
        {"name": "Apr", "sales": 2780},
        {"name": "May", "sales": 1890},
        {"name": "Jun", "sales": 2390},
        {"name": "Jul", "sales": 3490},
        {"name": "Aug", "sales": 2000},
        {"name": "Sep", "sales": 2780},
        {"name": "Oct", "sales": 1890},
        {"name": "Nov", "sales": 2390},
        {"name": "Dec", "sales": 3490},
    ]
    store_locations: list[str] = ["New York", "London", "Tokyo", "Paris"]
    selected_store: str = ""
    product_categories: list[str] = [
        "Electronics",
        "Apparel",
        "Groceries",
        "Home Goods",
        "Books",
    ]
    selected_categories: list[str] = []
    start_date: str = ""
    end_date: str = ""
    all_products: list[ProductData] = [
        {
            "id": 1,
            "name": "Quantum-Boost Sneakers",
            "units_sold": 120,
            "total_revenue": 18000.0,
        },
        {
            "id": 2,
            "name": "Chrono-Gauntlet Watch",
            "units_sold": 85,
            "total_revenue": 25500.5,
        },
        {
            "id": 3,
            "name": "Hydro-Dynamic Jacket",
            "units_sold": 250,
            "total_revenue": 37500.0,
        },
        {
            "id": 4,
            "name": "Aero-Graphene T-Shirt",
            "units_sold": 400,
            "total_revenue": 14000.0,
        },
        {
            "id": 5,
            "name": "Gravity-Defy Backpack",
            "units_sold": 150,
            "total_revenue": 11250.75,
        },
        {
            "id": 6,
            "name": "Stealth-Mode Sunglasses",
            "units_sold": 300,
            "total_revenue": 9000.0,
        },
        {
            "id": 7,
            "name": "Kinetic-Charge Shorts",
            "units_sold": 180,
            "total_revenue": 7200.0,
        },
        {
            "id": 8,
            "name": "Cryo-Compression Socks",
            "units_sold": 500,
            "total_revenue": 12500.0,
        },
        {
            "id": 9,
            "name": "Solar-Weave Hat",
            "units_sold": 220,
            "total_revenue": 5500.0,
        },
        {
            "id": 10,
            "name": "Bio-Mimicry Gloves",
            "units_sold": 130,
            "total_revenue": 4550.0,
        },
    ]

    @rx.var
    def filtered_and_sorted_products(self) -> list[ProductData]:
        products = self.all_products
        if self.product_search_query:
            search_lower = self.product_search_query.lower()
            products = [p for p in products if search_lower in p["name"].lower()]
        is_reverse = self.sort_order == "desc"
        return sorted(products, key=lambda p: p[self.sort_by], reverse=is_reverse)

    @rx.event
    def toggle_sidebar(self):
        """Toggles the collapsed state of the sidebar."""
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def set_time_granularity(self, new_granularity: str):
        self.time_granularity = new_granularity

    @rx.event
    def toggle_category(self, category: str):
        if category in self.selected_categories:
            self.selected_categories.remove(category)
        else:
            self.selected_categories.append(category)

    product_search_query: str = ""
    sort_by: str = "total_revenue"
    sort_order: str = "desc"

    @rx.event
    def set_product_search_query(self, query: str):
        self.product_search_query = query

    @rx.event
    def set_sorting(self, column: str):
        if self.sort_by == column:
            self.sort_order = "asc" if self.sort_order == "desc" else "desc"
        else:
            self.sort_by = column
            self.sort_order = "desc"