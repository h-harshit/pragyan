import { create } from "zustand";
import { immer } from "zustand/middleware/immer";
import { Tabs, TabType } from "@/shared/interfaces/tabs";

type TabsState = {
    tabs: Tabs
}

type TabsAction = {
    setCurrentTab: (currentTab: string) => void;
    setTabs: (tabs: Tabs) => void;
}

const initTabs = {
    currentTab: "Sheet 1", 
    allTabs:[
        {tabName: "Data Source", aliasName: "Data Source", tabType: "datasource" as TabType},
        {tabName: "Sheet 1", aliasName: "Sheet 1", tabType: "chart" as TabType}
    ]
}

export const useTabsDataStore = create<TabsState & TabsAction>()(immer((set)=>({
    tabs: initTabs,
    setCurrentTab: (currentTab: string) => {
        return set((state)=>{
            state.tabs.currentTab = currentTab
        })
    },
    setTabs: (newTabs: Tabs) => {
        return set((state)=> {
            state.tabs = newTabs
        })
    }
})))
