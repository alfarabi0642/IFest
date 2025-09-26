import SearchBar from "../SearchBar.jsx";
import Sort from "../Buttons/Sort.jsx";
import Filters from "../Buttons/Filters.jsx";
import Card from "../Card.jsx";
import Add from "../Buttons/Add.jsx";

function ContractList(){


    return (
        <div className="mt-5 ml-53 p-6 relative">
            <h1 className="text-2xl font-bold">Contract List</h1>
            <SearchBar/>
            <Filters/>
            <div className="flex justify-between ">
                <Sort/>
                <Add/>
            </div>
            <Card/>
            <Card/>
            <Card/>
            <Card/>

        </div>
    );
}

export default ContractList