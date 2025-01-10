import React from 'react'
import { FaRegArrowAltCircleLeft } from 'react-icons/fa'
import Button from "src/components/Button/Button"
import style from './error.module.css'
import DashboardBody from 'src/layouts/dashboard/DashboadBody';
import { useNavigate } from 'react-router-dom';
import { v4 } from "uuid"
import errorImage from '../../assets/images/500.svg'

const NotFound = () => {
    const navigate = useNavigate()
    return (
        <DashboardBody title="">
            <div className={style.error}>
                <img src={errorImage}></img>
                <div className={style.errorText}>
                    <h3>So Sorry, it's not you. it's us</h3>
                    <p>We are expreincing internal server problem. Please try again later.</p>
                    <Button className={style.iconButton} onClick={() => navigate(`/preview/${v4()}/chat`)} ><FaRegArrowAltCircleLeft />Go Back</Button>
                </div>
            </div>
        </DashboardBody>
    );
};

export default NotFound;