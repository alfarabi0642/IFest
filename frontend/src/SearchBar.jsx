import Search from "./assets/search_white.svg?react"
import Filter from "./assets/filter.svg?react"

function SearchBar(){
    return(
        <form className="rounded-full shadow-lg mr-107 mt-3 relative ">
            <div className="relative">
                <input type="search" placeholder="Search by Company, Year..." className="w-full p-3
                        rounded-full bg-white"/>
                <button className="absolute right-1 top-1/2 -translate-y-1/2 p-2.5 rounded-r-full bg-primary cursor-pointer">
                    <Search/>
                </button>
                <button className="absolute right-17 top-1/3 cursor-pointer">
                    <Filter/>
                </button>
            </div>
        </form>
    );

}

export default SearchBar