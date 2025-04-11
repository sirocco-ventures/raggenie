import { useEffect, useState } from 'react';
import { default as DropdownSelect } from 'react-select';
import style from './Select.module.css';



const Select = ({label, disabled = false , placeholder, options, value, hasError = false, errorMessage = "", onChange, noMargin, ...props}) => {
    const [selectedOption, setSelectedOption] = useState(null);

    const handleChange = (option) => {
        setSelectedOption(option);
        onChange(option)
    };

    useEffect(()=>{
        setSelectedOption(value)
    },[value])

    // Custom styles for the dropdown
    const customStyles = {
        control: (provided, state) => ({
            ...provided,
            color: '#DDDDDD',
            fontSize: "14px",
            fontFamily: 'Inter',
            backgroundColor: state.isFocused ? 'transparent' : 'transparent',
            borderColor: state.isFocused ? hasError ?   '#3893FF' : '#3893FF' : hasError ? "#FF7F6D" : '#F0F0F0',
            boxShadow: 'none',
            '&:hover': {
                borderColor: '#3893FF'
            }
        }),
        option: (provided, state) => ({
            ...provided,
            fontFamily: 'Inter',
            backgroundColor: state.isSelected ? '#FFF' : state.isFocused ? '#f0f0f0' : '#fff',
            color: state.isSelected ? '#5B5B5B' : state.isFocused ? '#333' : '#333',
            fontSize: "14px",
            padding: '10px',
            '&:hover': {
                backgroundColor: '#F9F9F9'
            }
        }),
        menu: (provided) => ({
            ...provided,
            backgroundColor: '#fff',
            border: '1px solid #ddd',
            borderRadius: '4px',
            boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)'
        }),
        menuList: (provided) => ({
            ...provided,
            padding: '0'
        }),
        singleValue: (provided) => ({
            ...provided,
            color: '#333'
        }),
        multiValue: (provided) => ({
            ...provided,
            backgroundColor: '#74B3FF',
            borderRadius: '20px',
            padding: '3px 4px',
            gap: '4px',
            border: 'none',
            display: 'flex',
            alignItems: 'center'

        }),
        indicatorSeparator: (provided) => ({
            ...provided,
            display: 'none'
        }),
        placeholder:(provided)=>({
            ...provided,
            color:"#888787"
        }),
        multiValueLabel: (provided) => ({
            ...provided,
            color: '#FFFFFF',
            fontSize: '14px',
            padding: '2px',
            fontFamily: 'Inter',
        }),
        multiValueRemove: (provided) => ({
            ...provided,
            color: '##84BCFF',
            backgroundColor: '#fff',
            cursor: 'pointer',
            height: '18px',
            width: '18px',
            borderRadius: '100%',
            ':hover': {
                backgroundColor: '#FF7F6D',
            }
        }),

    };

    return (
        <div className={`${noMargin ? '' : style.SelectContainer}`}>
            {noMargin ? '' : <h4 className={style.SelectLabel}>{label}</h4>}
            <DropdownSelect
                value={selectedOption}
                onChange={handleChange}
                options={options}
                placeholder={placeholder}
                isDisabled={disabled}
                styles={customStyles}
                {...props}

            />
             {errorMessage !== "" && <span className={style.ErrorMessage}>{errorMessage}</span>}
        </div>
    );
};

export default Select;