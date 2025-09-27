import ButtonSVG from '../src/assets/button.svg';

export default function Button() {
  return (
    <div className="flex justify-center items-center h-screen">
      <img src={ButtonSVG} alt="Apply Now" className="w-60 cursor-pointer" />
    </div>
  );
}
