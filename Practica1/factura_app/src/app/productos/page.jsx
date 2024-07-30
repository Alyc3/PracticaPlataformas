'use client';
import { useEffect, useState } from 'react';
import Link from "next/link";
import Sidebar from '../components/sideBar';
import { productos } from '@/hooks/Service_producto';
//import Menu from "../components/menu/menu.jsx";

export default function Producto() {
    let [productosList, setProductosList] = useState([]);
    let [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
    productos().then((info) => {
        if (info.code == '200') {
            setProductosList(info.datos);
            console.log(info.datos) 
        } else {
            console.error(info.datos.error);
        }
       });
    }, []);

    const filteredProductos = productosList.filter(productos => 
        productos.nombre?.toLowerCase().includes(searchTerm.toLowerCase()) || 
        productos.precio?.toString().toLowerCase().includes(searchTerm.toLowerCase())
        
    );

    return (
        <div style={{paddingLeft:"300px"}}>
            <Sidebar/>
            <main className="container text-center mt-5">
                <div className="col-4">
                    <Link href="/producto/new" style={{margin: "15px", marginRight: "265px", background: "#800020", border: "#800020", color: "#ffffff"}} className="btn btn-info">Agregar Producto</Link>
                </div>
                <div className="col-4">
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Buscar..."
                            style={{ width: "85%" }}
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                        <button className="btn btn-primary" style={{ width: "20%", marginLeft: "5%" }}>Buscar</button>
                    </div>
                </div>
                <div className="container-fluid" style={{ marginTop: "2%" }}>
                    <table className="table table-hover">
                        <thead className="table-dark">
                            <tr>
                                <th>Nro</th>
                                <th>Producto</th>
                                <th>Descripcion</th>
                                <th>Precio</th>
                                <th>Stock</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                        {filteredProductos.map((productos, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{productos.nombre}</td>
                                    <td>{productos.descripcion}</td>
                                    <td>{productos.precio}</td>
                                    <td>{productos.stock}</td>
                                    
                                    <td>
                                        {/* Ajusta esta parte según las acciones que desees permitir */}
                                        <Link href={`/producto`} className="btn btn-primary">Editar</Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <div style={{ height: "500px", marginTop: "2%", border: "1px solid #000" }}>
            </div>  
            </main>
        </div>
    );
}