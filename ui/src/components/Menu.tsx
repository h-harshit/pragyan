import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarShortcut,
  MenubarTrigger,
} from "./ui/menubar"

const Menu = () => {
  return (
    <Menubar className="h-[1.8rem] mt-0 border-0">
      <MenubarMenu>
        <MenubarTrigger>File</MenubarTrigger>
        <MenubarContent className="bg-white">
          <MenubarItem>
            New<MenubarShortcut>Ctrl+N</MenubarShortcut>
          </MenubarItem>
          <MenubarItem>
            New Tab<MenubarShortcut>Ctrl+T</MenubarShortcut>
          </MenubarItem>
          <MenubarItem>
            Open...<MenubarShortcut>Ctrl+O</MenubarShortcut>
          </MenubarItem>
        </MenubarContent>
      </MenubarMenu>
      <MenubarMenu>
        <MenubarTrigger>Edit</MenubarTrigger>
      </MenubarMenu>
      <MenubarMenu>
        <MenubarTrigger>View</MenubarTrigger>
      </MenubarMenu>
      <MenubarMenu>
        <MenubarTrigger>Help</MenubarTrigger>
      </MenubarMenu>
    </Menubar>
  )
}

export default Menu
