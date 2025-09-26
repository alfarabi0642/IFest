import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Home_Off from "./assets/home_off.svg?react";
import Home_On from "./assets/home_on.svg?react";
import Search_On from "./assets/search_on.svg?react";
import Search_Off from "./assets/search_off.svg?react";
import Draft_On from "./assets/draft_on.svg?react";
import Draft_Off from "./assets/draft_off.svg?react";
import Review_On from "./assets/review_on.svg?react";
import Review_Off from "./assets/review_off.svg?react";
import Notif_On from "./assets/notif_on.svg?react";
import Notif_Off from "./assets/notif_off.svg?react";
import Reports_On from "./assets/reports_on.svg?react";
import Reports_Off from "./assets/reports_off.svg?react";
import Profile from "./Profile.jsx";

const sidebarItems = [
  { label: "home", text: "Home Page", path: "/", IconOn: Home_On, IconOff: Home_Off },
  { label: "list", text: "Contract List", path: "/contracts", IconOn: Search_On, IconOff: Search_Off },
  { label: "draft", text: "Contract Drafts", path: "/drafts", IconOn: Draft_On, IconOff: Draft_Off },
  { label: "review", text: "Contract Reviews", path: "/reviews", IconOn: Review_On, IconOff: Review_Off },
  { label: "notif", text: "Notifications", path: "/notifications", IconOn: Notif_On, IconOff: Notif_Off },
  { label: "reports", text: "Reports", path: "/reports", IconOn: Reports_On, IconOff: Reports_Off },
];

function SidebarItem({ item, isActive, onClick }) {
  const { IconOn, IconOff, text } = item;

  return (
    <div
      onClick={onClick}
      className={`flex items-center mx-2 my-1 p-2 rounded-xl cursor-pointer transition-colors duration-200
                  ${isActive ? "bg-blue-100 text-blue-600" : "text-gray-600 hover:bg-gray-100"}`}
    >
      <div className="flex items-center justify-center h-10 w-10">
        {isActive ? <IconOn className="w-6 h-6" /> : <IconOff className="w-6 h-6" />}
      </div>
      <p className="ml-2 font-poppinsbold">{text}</p>
    </div>
  );
}

function Sidebar() {
  const [active, setActive] = useState("home");
  const navigate = useNavigate();

  return (
    <div className="fixed top-0 left-0 h-screen w-[35vh] 
                   flex flex-col shadow-2xl
                   pt-4 bg-white">
      <h1 className="p-2 mt-2 text-center text-[5vh] text-primary font-poppinsbold">ILC<a className="text-black">Sense</a></h1>
      
      <nav className="mt-1">
        {sidebarItems.map((item) => (
          <SidebarItem
            key={item.label}
            item={item}
            isActive={active === item.label}
            onClick={() => {
              setActive(item.label);
              navigate(item.path);
            }}
          />
        ))}
      </nav>

      <div className="mt-auto p-2">
        <Profile username="Ishaq Irfan F" role="Contract Manager" />
      </div>
    </div>
  );
}

export default Sidebar;