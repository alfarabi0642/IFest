import { useState } from "react";
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
import { useNavigate } from "react-router-dom";


/*
function Sidebar(){
    return (
        <div className="fixed top-0 left-0 h-screen w-16 m-0
                        flex flex-col bg-gray-900 text-white
                         shadow-2xl" >
            
            <SidebarIcon icon={<Home_Off className="w-7 h-7 text-white p-2" />} />
        </div>
    );
}

const SidebarIcon = ({ icon }) => (
    <div className="sidebar-icon">
        {icon}
    </div>
);
*/

function Sidebar() {
  const [active, setActive] = useState("home"); // track active menu

  return (
    <div className="fixed top-0 left-0 h-screen w-30 
                    flex flex-col shadow-2xl
                    pt-4">
      <h1 className="p-2 text-center text-[3vh] text-primary font-poppinsbold">ILC<a className="text-black">Sense</a></h1>
      <SidebarIcon
        label="home"
        active={active}
        setActive={setActive}
        IconOff={Home_Off}
        IconOn={Home_On}
        path="/"
      />

      <SidebarIcon
        label="list"
        active={active}
        setActive={setActive}
        IconOff={Search_Off}
        IconOn={Search_On}
        path="/contracts"
      />

      <SidebarIcon
        label="draft"
        active={active}
        setActive={setActive}
        IconOff={Draft_Off}
        IconOn={Draft_On}
      />

      <SidebarIcon
        label="review"
        active={active}
        setActive={setActive}
        IconOff={Review_Off}
        IconOn={Review_On}
      />

      <SidebarIcon
        label="notif"
        active={active}
        setActive={setActive}
        IconOff={Notif_Off}
        IconOn={Notif_On}
      />

      <SidebarIcon
        label="reports"
        active={active}
        setActive={setActive}
        IconOff={Reports_Off}
        IconOn={Reports_On}
      />


      {/* you can add more items like: 
          <SidebarIcon label="settings" IconOff={Settings_Off} IconOn={Settings_On} ... /> */}
    </div>
  );
}

function SidebarIcon({ label, active, setActive, IconOff, IconOn, path }) {
  const isActive = active === label;
  const navigate = useNavigate();

  return (
    <div
      className={`relative flex items-center justify-center h-13 w-11 mt-2 mb-2 mx-auto 
                  rounded-3xl cursor-pointer transition-all duration-400 hover:rounded-xl
                  ${isActive ? "bg-gray-800" : " bg-gray-500 text-gray-400"}`}
      onClick={() => {
        setActive(label);
        navigate(path);
      }}
    >
      {isActive ? (
        <IconOn className="w-5 h-5" />
      ) : (
        <IconOff className="w-5 h-5" />
      )}
    </div>
  );
}

export default Sidebar