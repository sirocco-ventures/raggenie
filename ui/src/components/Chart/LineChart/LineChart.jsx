
import { LineChart as ReLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import style from "../style.module.css"


const LineChart = ({title ="Line Chart", data = [], xAxis = "name", yAxis = "value", dataLength = 12})=>{

    const customXAxisLabel = ({ payload, x, y, width, height })=>{
       
        return(
            <text orientation="bottom" width={width} height={height} stroke="none" x={x} y={y + 10}  style={{direction:"rtl",fontSize:"11px",fontFamily:"Inter",color:"rgba(28, 28, 28, 0.40",textAlign:"center",fontStyle:"normal", fontWeight:"300", lineHeight:"18px",opacity:"60%"}} fill="#888787" >
                <tspan x={x+20} y={y+10}>{payload.value}</tspan>
            </text>
        )
    }

    const customYAxisLabel = ({ payload, x, y, width, height })=>{
        
        return(
            <text orientation="bottom" width={width} height={height} stroke="none" x={x} y={y + 10}  style={{direction:"rtl", fontSize:"11px",fontFamily:"Inter",color:"rgba(28, 28, 28, 0.40",textAlign:"center",fontStyle:"normal",fontWeight:"300", lineHeight:"18px", opacity:"60%"}} fill="#888787">
                <tspan x={x-5} y={y}>{payload.value}</tspan>
            </text>
        )
    }


    return(
        <>
            <div className={style.ChartContainer}>
                <span className={style.ChartTitle}>{title}</span>
                <div className={style.BarChartResponsive}>
                <ResponsiveContainer  width={450} height={183} >
                    <ReLineChart  data={data.slice(0, dataLength)}>
                        <CartesianGrid vertical={false} strokeDasharray="3 3" />
                        <XAxis dataKey={xAxis}   axisLine={false} tickLine={false} tick={customXAxisLabel} />
                        <YAxis  axisLine={false} tickLine={false} tick={customYAxisLabel} />
                        <Tooltip/>
                        <Line type="monotone" dataKey={yAxis} stroke="#3893FF" strokeWidth={3} />
                    </ReLineChart>
                </ResponsiveContainer>
                </div>
            </div>
        
        </>
    )

}


export default LineChart