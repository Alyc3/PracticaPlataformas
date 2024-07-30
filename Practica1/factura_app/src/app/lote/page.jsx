'use client';
import { useEffect, useState } from 'react';
import Link from "next/link";
import { lotes } from '@/hooks/Service_lote';
import Sidebar from '../components/sideBar';
//import Menu from "../components/menu/menu.jsx";

export default function Lote() {
    let [lotesList, setLotesList] = useState([]);
    let [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
    lotes().then((info) => {
        if (info.code == '200') {
            setLotesList(info.datos);
            console.log(info.datos) 
        } else {
            console.error(info.datos.error);
        }
       });
    }, []);

    const filteredLotes = lotesList.filter(lotes => 
        lotes.nombrePr?.toLowerCase().includes(searchTerm.toLowerCase()) || 
        lotes.estadoPr?.toLowerCase().includes(searchTerm.toLowerCase())
        
    );

    return (
        <div style={{paddingLeft:"300px"}}>
            <Sidebar/>
            <main className="container text-center mt-5">
                <div className="col-4">
                    <Link href="/lote/new" style={{margin: "15px", marginRight: "265px", background: "#800020", border: "#800020", color: "#ffffff"}} className="btn btn-info">Agregar Lote</Link>
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
                                <th>Nombre del Producto</th>
                                <th>Fecha de Vencimiento</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                        {filteredLotes.map((lote, index) => (
                                <tr key={index}>
                                    <td>{index + 1}</td>
                                    <td>{lote.nombrePr}</td>
                                    <td>{new Date(lote.fechaVen).toLocaleDateString('es-ES')}</td>
                                    <td>{lote.estadoPr}</td>
                                    
                                    <td>
                                        {/* Ajusta esta parte según las acciones que desees permitir */}
                                        <Link href={`/lote/${lote.external_id}`} className="btn btn-primary">Editar</Link>
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