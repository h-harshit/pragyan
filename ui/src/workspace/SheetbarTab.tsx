import React, { useState } from 'react'
import { SegmentedControl } from '@radix-ui/themes'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Input } from "@/components/ui/input";
import { ContextMenu, ContextMenuContent, ContextMenuItem, ContextMenuTrigger } from '@/components/ui/context-menu';
import { Tab } from '@/shared/interfaces/tabs';

interface ISheetbarTab {
    tab: Tab;
    tabIndex: number;
    handleTabClick: (tabIndex: number) => void
}
const SheetbarTab:React.FC<ISheetbarTab> = ({tab, tabIndex, handleTabClick}) => {
    const [inputTabAliasName, setInputTabAliasName] = useState<string|undefined>(tab?.aliasName)
    return (
    <SegmentedControl.Item onClick={() => handleTabClick(tabIndex)} key={tabIndex} value={tab.tabName}>
                            <ContextMenu>
                                <ContextMenuTrigger className="flex items-center justify-center h-full w-full">
                                    <div className="mx-1">{tab.aliasName}</div>
                                </ContextMenuTrigger>
                                <ContextMenuContent className="bg-white mb-[1.8rem] min-w-[5rem] border-[#e5e7eb] rounded-[5px]">
                                    <Popover>
                                        <PopoverTrigger>
                                            <ContextMenuItem inset className="p-1 cursor-pointer">
                                                Rename
                                            </ContextMenuItem>
                                            <PopoverContent className="w-80">
                                                <div className="flex flex-col gap-2">
                                                    <h4 className="font-medium leading-none">Rename Sheet</h4>
                                                    <Input
                                                        id="width"
                                                        value={inputTabAliasName}
                                                        onChange={(event)=>setInputTabAliasName(event?.target.value)}
                                                        className="col-span-2 h-8"
                                                    />

                                                </div>
                                            </PopoverContent>
                                        </PopoverTrigger>
                                    </Popover>
                                    <ContextMenuItem inset className="p-1 cursor-pointer">
                                        Delete
                                    </ContextMenuItem>
                                </ContextMenuContent>
                            </ContextMenu>
                        </SegmentedControl.Item>
    )
    }

export default SheetbarTab