import { PieChart as RePieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import style from '../style.module.css';


const COLORS = ['#3893FF', '#84BCFF', '#CDE5FF', '#FF8042'];

const CustomLegend = (props) => {
    const { payload, label } = props;
    return (
        <div>
            {payload.map((entry, index) => (
                <div key={`item-${index}`} className={style.PieLegend}>
                    <div>
                        <svg width={20} height={20} style={{ borderRadius:"3px", display: 'inline-block', marginRight: '5px' }}>
                            <rect width={20} height={20} fill={entry.color} />
                        </svg>
                    </div>
                    <div>
                        {entry.payload[label]}
                    </div>
                </div>
            ))}
        </div>
    );
};


const PieChart = ({ title = "Pie Chart", data = [] , dataKey= "value", labelKey="label", dataLength = 12 }) => {
  return (
    <>
         <div className={style.ChartContainer}>
        <span className={style.ChartTitle}>{title}</span>
          <div className={style.BarChartResponsive}>
            <ResponsiveContainer width={450} height={183}>
              <RePieChart>
                <Pie
                  data={data?.slice(0, dataLength)}
                  labelLine={false}
                  innerRadius={0}
                  dataKey={dataKey}
                  stroke=""
                >
                  {data.map((entry, index) => (
                    <Cell key={entry[labelKey]} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend content={<CustomLegend label={labelKey} />} layout="vertical" align="right" verticalAlign="middle"  wrapperStyle={{top: "0px", height: "200px", overflow: "auto"}} />
              </RePieChart>
            </ResponsiveContainer>  
          </div>
        </div>
    </>
  );
};

export default PieChart;
