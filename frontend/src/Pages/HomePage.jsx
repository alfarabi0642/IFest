import Card from "../Card.jsx";
import Button from "../Button.jsx"

function HomePage(){
    return (
        <div className="ml-20 p-6">
            <h1 className="text-2xl font-bold">Home Page</h1>
            <Card nama_perusahaan="Google"/>
            <Button />
        </div>
    );
}
export default HomePage