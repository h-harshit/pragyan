import React from 'react'
import { SegmentedControl } from '@radix-ui/themes'
import { useTabsDataStore } from "@/store"
import { MdAddchart, MdOutlineDashboardCustomize   } from "react-icons/md";
import { Button } from '@/components/ui/button';
import { RiPresentationLine } from "react-icons/ri";
import { produce } from 'immer';
import { TabType } from '@/shared/interfaces/tabs';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import SheetbarTab from './SheetbarTab';


const Sheetbar: React.FC = () => {
    const tabs = useTabsDataStore((state)=>state.tabs)
    const currentTab = tabs?.currentTab
    const allTabs = tabs.allTabs

    const setCurrentTab = useTabsDataStore((state)=>state.setCurrentTab)
    const setTabs = useTabsDataStore((state)=>state.setTabs)

    const getNewTabName = (tabType: Exclude<TabType,"datasource">, newTabCount: number) => {
        if(tabType==="chart") {
            return `Sheet ${newTabCount}`
        } else if(tabType==="dashboard") {
            return `Dashboard ${newTabCount}`
        } else if(tabType === "presentation") {
            return `Presentation ${newTabCount}`
        }
    }
    const handleAddTab = (tabType: Exclude<TabType,"datasource">) => {
        const tabCount = allTabs.filter((tab)=>tab.tabType===tabType).length
        const newTabName = getNewTabName(tabType, tabCount+1)
        if(!newTabName) return
        const newTabObj = {
            tabName: newTabName,
            aliasName: newTabName,
            tabType: tabType
        }

        const newTabs = produce(tabs, (draft)=>{
            draft["allTabs"].push(newTabObj)
        })

        setTabs(newTabs)
        setCurrentTab(newTabName)
    }

    const handleTabClick = (tabIndex:number) => {
        const clickedTabName = allTabs[tabIndex].tabName
        setCurrentTab(clickedTabName)
    }

    return (
        <div className="fixed bottom-0 left-0 right-0 w-full bg-[#e7e7eb]">
            <SegmentedControl.Root value={currentTab} size="1" variant="classic">
                {allTabs.map((tab, tabIndex)=>{
                    return(
                        <SheetbarTab tab={tab} tabIndex={tabIndex} handleTabClick={handleTabClick}/>
                    )
                })}
            </SegmentedControl.Root>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Button variant="outline" size="icon" className="h-[23px] bg-white border-[1px] border-[#e5e7eb] rounded-[4px] hover:bg-white" onClick={()=>handleAddTab("chart")}><MdAddchart/></Button>
                    </TooltipTrigger>
                    <TooltipContent className="border-[1px] border-[#e5e7eb] p-1 rounded-[4px] text-[10px] text-gray-700">
                        <p>New Sheet</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Button variant="outline" size="icon" className="h-[23px] bg-white border-[1px] border-[#e5e7eb] rounded-[4px] hover:bg-white" onClick={()=>handleAddTab("dashboard")}><MdOutlineDashboardCustomize /></Button>
                    </TooltipTrigger>
                    <TooltipContent className="border-[1px] border-[#e5e7eb] p-1 rounded-[4px] text-[10px] text-gray-700">
                        <p>New Dashboard</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Button variant="outline" size="icon" className="h-[23px] bg-white border-[1px] border-[#e5e7eb] rounded-[4px] hover:bg-white" onClick={()=>handleAddTab("presentation")}><RiPresentationLine/></Button>
                    </TooltipTrigger>
                    <TooltipContent className="border-[1px] border-[#e5e7eb] p-1 rounded-[4px] text-[10px] text-gray-700">
                        <p>New Presentation</p>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>
        </div>
    )
}

export default Sheetbar