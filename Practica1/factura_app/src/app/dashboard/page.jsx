'use client';
import { all_personas } from '@/hooks/Services_persona';
import Cookies from 'js-cookie';
//import Menu from '../components/menu/menu';
import Sidebar from '../components/sideBar';
import  "bootstrap/dist/css/bootstrap.min.css"

export default function Dashboard(){
  /*let token = Cookies.get('token');
  //console.log(token);
    all_personas(token).then((info) =>{
      console.log(info);
    })*/
    return (
      <div >
        <Sidebar>
          <div>
            Bienvenido
          </div>
        </Sidebar>
      </div>
    );
}