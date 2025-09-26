import Search from "./assets/search_white.svg?react"

function SearchBar(){
    return(
        <form className="w-[440px] mt-3 relative ">
            <div className="relative">
                <input type="search" placeholder="Search by Company, Year..." className="w-full p-4
                        rounded-full bg-white"/>
                <button className="absolute right-1 top-1/2 -translate-y-1/2 p-3.5 rounded-r-full bg-primary ">
                    <Search/>
                </button>
            </div>
        </form>
    );

}

export default SearchBar