
import { Bar, BarChart as ReBarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import style from "../style.module.css"

const BarChart = ({title ="Bar Chart", data = [], xAxis = "name", yAxis = "value",  dataLength = 12,})=>{


    const customBar = (props)=>{
        const {x, y, height } = props;
       return (
            <rect width={"28"} height={height} x={x + 10} y={y} fill="#74B3FF" rx="4"></rect>
        )
    }

    const customAxisLabel = ({ payload, x, y, width, height })=>{
        return(
            <text orientation="bottom" width={width} height={height} stroke="none" x={x} y={y + 40}  textAnchor="middle" style={{fontSize:"11px",fontFamily:"Inter",color:"rgba(28, 28, 28, 0.40",textAlign:"center",fontStyle:"normal", fontWeight:"300", lineHeight:"18px",opacity:"60%"}} fill="#888787">
                <tspan x={x} y={y + 12}>{payload.value}</tspan>
            </text>
        )
    }

    return(
        <>
            <div className={style.ChartContainer}>
                <span className={style.ChartTitle}>{title}</span>
               
                <div className={style.BarChartResponsive}>
                <ResponsiveContainer width={500} height={183}>
                        <ReBarChart  data={data.slice(0, dataLength)} barCategoryGap={0} barGap={5}>
                            <XAxis dataKey={xAxis} axisLine={false} tickLine={false} tick={customAxisLabel} />
                            <YAxis axisLine={false} tickLine={false} tick={customAxisLabel} />
                            <Bar dataKey={yAxis} shape={customBar} />
                            <Tooltip cursor={false}  />
                        </ReBarChart>
                    </ResponsiveContainer>
                </div>
                
            </div>
        
        </>
    )

}


export default BarChart