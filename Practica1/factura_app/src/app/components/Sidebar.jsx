'use client';
import { useRouter } from 'next/navigation';
import Link from 'next/link'
import { SlBag, SlBasket, SlHome,SlLogout } from 'react-icons/sl';
import { BsInfoSquare, BsEnvelope } from 'react-icons/bs'; // Corrección de 'BsEnvelopeAt' a 'BsEnvelope'
import { FaTshirt, FaRedhat } from 'react-icons/fa';

export default function Sidebar({ show, setter }) {
    const router = useRouter();

    // Define our base class
    const className = "bg-black w-[250px] transition-[margin-left] ease-in-out duration-500 fixed top-0 bottom-0 left-0 z-40 h-screen";
    // Append class based on state of sidebar visibility
    const appendClass = show ? " ml-0" : " ml-[-300px] md:ml-0";

    // Clickable menu items
    const MenuItem = ({ icon, name, route }) => {
        // Highlight menu item based on currently displayed route
        const colorClass = router.pathname === route ? "text-white" : "text-white/50 hover:text-white";

       return (
        <Link href={route} passHref>
            <div
                onClick={() => setter(oldVal => !oldVal)}
                className={`flex gap-2 items-center text-md pl-6 py-3 border-b-[1px] border-b-white/10 cursor-pointer ${colorClass}`}
            >
                <div className="text-xl">
                    {icon}
                </div>
                <span>{name}</span>
            </div>
        </Link>
    );
};
    // Overlay to prevent clicks in background, also serves as our close button
    const ModalOverlay = ({ name, route, icon }) => (
        <div
            className={`fixed inset-0 bg-white/50 z-30`}
            onClick={() => setter(oldVal => !oldVal)}
        />
    );

    return (
        <>
        
            <div className={`${className}${appendClass}`}>
                <div className="flex flex-col">
                    <MenuItem
                        name="Home"
                        route="/"
                        icon={<SlHome />}
                    />
                    <MenuItem
                        name="Registrar Lotes"
                        route="/lote"
                        icon={<SlBag />}
                    />
                    <MenuItem
                        name="Registrar Productos"
                        route="/producto"
                        icon={<SlBasket />}
                    />
                    <MenuItem
                    
                        name="Cerrar sesion"
                        route="/contact"
                        icon={<SlLogout />}
                    />
                </div>
            </div>
            {show && <ModalOverlay />}
        </>
    );
}