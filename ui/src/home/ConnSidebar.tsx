import React from 'react';
import { LucideCirclePlus, LucideFile, ChevronRight, LucideDatabase } from 'lucide-react';
import { Button } from '@/components/ui/button';
// import { Separator } from '@/components/ui/separator';
import { 
  SidebarProvider,
  Sidebar,
  SidebarInset,
  SidebarHeader,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton
} from '@/components/ui/sidebar';

import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent
} from "@/components/ui/collapsible"

import { Link } from 'react-router-dom'

const sidebarItems = [
    {
      title: "File",
      url: "#",
      icon: LucideFile,
      isActive: true,
      items: [
        {
          title: "CSV",
          url: "#",
        },
        {
          title: "Microsoft Excel",
          url: "#",
        },
        {
          title: "JSON",
          url: "#",
        },
        {
          title: "Parquet",
          url: "#",
        },
      ],
    },
    {
      title: "Database",
      url: "#",
      icon: LucideDatabase,
      items: [
        {
          title: "Microsoft SQL Server",
          url: "#",
        },
        {
          title: "PostgreSQL",
          url: "#",
        },
        {
          title: "MySQL",
          url: "#",
        },
      ],
    },
  ]

const ConnSidebar:React.FC = () => {
  return (
    // <div className="fixed left-0 top-[1.8rem] bottom-0 w-[20%] h-full border-r border-gray-200">
    //   <div className="flex flex-col">
        <SidebarProvider className='min-h-[calc(100vh-1.9rem)]'>
          <Sidebar collapsible='icon' className='top-[1.9rem] bg-white'>
            <SidebarHeader>
              <div className="flex flex-row justify-start align-center p-3 mt-4">
                <Button className="rounded-[5px] bg-black text-white hover:bg-gray-700 h-7">
                  <LucideCirclePlus className="font-normal"/> Add Connection
                </Button>
               </div>
            </SidebarHeader>
            <SidebarContent>
              <SidebarGroup>
                <SidebarGroupLabel className="mx-1 text-base">Connect to</SidebarGroupLabel>
                <SidebarMenu>
                  {sidebarItems.map((item)=>{
                    return(
                      <Collapsible
                        key={item.title}
                        asChild={true}
                        defaultOpen={item.isActive}
                        className="group/collapsible"
                      >
                        <SidebarMenuItem>
                          <CollapsibleTrigger asChild={true}>
                            <SidebarMenuButton tooltip={item.title}>
                              {item.icon && <item.icon/>}
                              <span>{item.title}</span>
                              <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                            </SidebarMenuButton>
                          </CollapsibleTrigger>
                          <CollapsibleContent>
                            <SidebarMenuSub>
                              {item.items?.map((subItem)=>{
                                return(
                                  <SidebarMenuSubItem key={subItem.title}>
                                    <SidebarMenuSubButton asChild={true}>
                                      <a href={subItem.url}>
                                        <span>{subItem.title}</span>
                                      </a>
                                    </SidebarMenuSubButton>
                                  </SidebarMenuSubItem>
                                )
                              })}
                            </SidebarMenuSub>
                          </CollapsibleContent>
                        </SidebarMenuItem>
                      </Collapsible>
                    )
                  })}
                </SidebarMenu>
              </SidebarGroup>
            </SidebarContent>
          </Sidebar>
          <SidebarInset className='mt-[2rem] ml-[2rem]'>
            <div className='text-lg font-medium mb-8'>Open</div>
            <Link to="/workspace">
              <div className='flex flex-row justify-center items-center text-[1rem] font-medium border rounded-xl border-gray-300 shadow-md p-4 rounded-md w-[8rem] h-[8rem]'>
                Blank Workspace
              </div>
            </Link>
          </SidebarInset>
        </SidebarProvider>
    //   </div>
    // </div>
  )
}

export default ConnSidebar