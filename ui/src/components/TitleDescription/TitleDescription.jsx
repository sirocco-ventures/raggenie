import style from './TitleDescription.module.css';

const TitleDescription = ({
  title = "",
  description = "",
  className = "",
  headingClass = "",
  showOrder = false ,
  descriptionClass = "",
  orderNumber = 0,
  ...props
})=>{
    return (
    <div className={`${style.TitleContainer} ${className}`} {...props}>
      {showOrder ? ( <div className={style.CountNumber}>{orderNumber}</div>):(null)}
      <div>
        <h3 className={`${style.Title} ${headingClass}`}>{title}</h3>
        <p className={`${style.Description} ${descriptionClass}`}>{description}</p>
      </div>
    </div>
    )
}

export default TitleDescription;
