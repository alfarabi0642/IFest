import ArrowDown from "../assets/arrow_down.svg?react";
import { useState } from "react";


function Sort(){

    const [isOpen, setIsOpen] = useState(false);
    function toggleDropdown() {
        setIsOpen(!isOpen); 
  }

    return(
        <div className="relative select-none ml-2" id="dropdownButton">
            <div onClick={toggleDropdown} className=" text-sm bg-white hover:shadow-md flex justify-between border-solid border-black border-1 
                            rounded-full py-1.5 px-4 cursor-pointer font-poppins h-6 w-20 items-center mt-5"> 
                Sort
                <ArrowDown/>
            </div>
            {isOpen && (
                <div>
                    <div id="newest" className="hover:text-white flex items-center h-8 transition-all hover:bg-secondary rounded-full bg-white absolute top-12 border-1 w-40 border-gray-400 shadow-md">
                        <div className="cursor-pointer px-5 ">Newest</div>
                    </div>
                    <div id="oldest" className="hover:text-white flex items-center h-8 transition-all hover:bg-secondary rounded-full bg-white absolute top-21 border-1 w-40 border-gray-400 shadow-md">
                        <div className="cursor-pointer px-5 ">Oldest</div>
                    </div>
                </div>
            )}
        </div>
    );
}   

export default Sort