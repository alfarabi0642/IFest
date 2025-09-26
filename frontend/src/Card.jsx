import defaultLogo from "./assets/googleicon.png"
import Location from "./assets/Location.svg?react"
import Eye from "./assets/view.svg?react"
import Bookmark from "./assets/bookmark.svg?react"
import ThreeDots from "./assets/three_dots.svg?react"  


function Card ({logo=defaultLogo, 
                judul_kontrak="Development Partnership Agreement", 
                perihal_kontrak="Mobile App Hackathon", 
                nama_perusahaan="PT Innovatech Indonesia",
                lokasi="Bandung, Indonesia",
                kategori="Partnership",
                status="Unapproved",
                periode=" 1 Sep - 1 Okt 2025",
                value="IDR 20.000.000"
                }){
    return (
        <div className="flex rounded-3xl h-auto border-0 p-5 mt-4 mb-7 mr-106 shadow-indigo-300 shadow-lg" >
            <div className="bg-blue-200 items-center justify-center h-26 w-26 flex">
                <img src={logo} alt="Logo Perusahaan" ></img>
            </div>
            <div className="ml-5 flex-col">
                <h1 className="font-poppinsbold text-2xl ">{nama_perusahaan}</h1>
                <h2 className="font-poppins text-gray-500 mt-1">{judul_kontrak}</h2>
                <div className="flex items-center mt-2 text-gray-500">
                    <Location className="mr-1"/>
                    <p className=" font-poppins text-sm text-gray-500">{lokasi}</p>
                    <Eye className="mr-1 ml-4"/>
                    <p className="font-poppins text-sm text-gray-500">{kategori}</p>
                </div>
            </div>
            <div className="flex-col ml-14 mt-4 w-55">
                <p className="mb-2 text-sm font-poppins text-gray-500">Status: {status}</p>
                <p className="font-poppins text-md">{periode}</p>
                <p className="font-poppinsbold text-primary text-lg mt-2">{value}<a className=" ml-1 font-poppins text-gray-500 text-sm">/ month</a></p>
            </div>

            <div className="flex justify-center mb-auto">
                <button>
                    <Bookmark className="ml-3 mr-3"/>
                </button>
                <button>
                    <ThreeDots className="ml-3"/>
                </button>
            </div>

        </div>
    );
}

export default Card