import  React  from 'react';
const TitleDescriptionContainer = ({ children }) => {
    return (
       <>
       {React.Children.map(children, (child, index) => {
            if(React.isValidElement(child)){
                return React.cloneElement(child, { showOrder: true, })
            }
        })}
       </>
    );
};

export default TitleDescriptionContainer