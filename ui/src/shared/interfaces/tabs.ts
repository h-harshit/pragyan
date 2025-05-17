export type TabType = "datasource" | "chart" | "dashboard" | "presentation"

export type Tab = {
    tabName: string;
    aliasName: string;
    tabType: TabType;
}

export type Tabs = {
    currentTab: string;
    allTabs: Tab[];
}