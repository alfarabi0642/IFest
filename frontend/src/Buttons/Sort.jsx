import ArrowDown from "../assets/arrow_down.svg?react";
import { useState } from "react";


function Sort(){

    const [isOpen, setIsOpen] = useState(false);
    function toggleDropdown() {
        setIsOpen(!isOpen); 
  }

    return(
        <div className="relative select-none" id="dropdownButton">
            <div onClick={toggleDropdown} className=" flex justify-between border-solid border-black border-1 
                            rounded-full py-1.5 px-4 cursor-pointer font-poppins w-30 items-center mt-5"> 
                Sort
                <ArrowDown/>
            </div>
            {isOpen && (
                <div>
                    <div id="newest" className=" transition-all hover:bg-primary rounded-full bg-white absolute top-11.5 border-1 w-50 border-gray-400 shadow-md">
                        <div className="cursor-pointer py-2 px-5 hover:text-white">Newest</div>
                    </div>
                    <div id="oldest" className=" transition-all hover:bg-primary rounded-full bg-white absolute top-23 border-1 w-50 border-gray-400 shadow-md">
                        <div className="cursor-pointer py-2 px-5 hover:text-white">Oldest</div>
                    </div>
                </div>
            )}
        </div>
    );
}   

export default Sort