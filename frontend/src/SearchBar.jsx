// src/SearchBar.jsx

import Search from "./assets/search_white.svg?react";
import Filter from "./assets/filter.svg?react";

// The component now accepts props in its function signature
function SearchBar({ searchTerm, onSearchChange, onSearchSubmit }) {
    
    // This function prevents the page from reloading on enter/submit
    const handleSubmit = (event) => {
        event.preventDefault(); 
        onSearchSubmit();
    };

    return (
        <form onSubmit={handleSubmit} className="rounded-full shadow-lg mr-107 mt-3 relative ">
            <div className="relative">
                <input 
                    type="search" 
                    placeholder="Search by Company, Year, or contract content..." 
                    className="w-full p-3 rounded-full bg-white"
                    // The input's value is now controlled by the parent's state
                    value={searchTerm}
                    // When the user types, it calls the function from the parent
                    onChange={onSearchChange}
                />
                <button type="submit" className="absolute right-1 top-1/2 -translate-y-1/2 p-2.5 rounded-r-full bg-primary cursor-pointer">
                    <Search />
                </button>
                <button type="button" className="absolute right-17 top-1/3 cursor-pointer">
                    <Filter />
                </button>
            </div>
        </form>
    );
}

export default SearchBar;