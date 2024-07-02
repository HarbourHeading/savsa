import {useEffect, useRef} from "react"
import PropTypes from 'prop-types'
import styles from './YearSlider.module.css'

function YearSlider({min, max, inputValue, setInputValue, step}) {

    let sliderRef = useRef(null)

    function handleSlider() {
        setInputValue(parseInt(sliderRef.current.value))
    }

    function handleNumber(event) {
        let newValue = parseInt(event.target.value)

        if (newValue < min) {
            setInputValue(min)
        } else if (newValue > max) {
            setInputValue(max)
        } else {
            setInputValue(newValue)
        }
    }

    useEffect(() => {
        handleSlider()
    })

    return (
        <div>
            <div className={styles.yearSlider}>
                <div className={styles.yearSlider__values}>
                    <small>{min}</small>
                    <input
                        type="number"
                        className={styles.yearSlider__numberInput}
                        onInput={handleNumber}
                        value={inputValue}
                        min={min} max={max}
                        step={step}
                    />
                    <small>{max}</small>
                </div>
                <div className={styles.yearSlider__container}>
                    <input
                        type="range"
                        className={styles.yearSlider__slider}
                        value={inputValue}
                        min={min} max={max}
                        ref={sliderRef} step={step}
                        onInput={handleSlider}
                    />
                </div>
            </div>
        </div>
    )
}

YearSlider.propTypes = {
    min: PropTypes.number.isRequired,
    max: PropTypes.number.isRequired,
    inputValue: PropTypes.number.isRequired,
    setInputValue: PropTypes.func.isRequired,
    step: PropTypes.number.isRequired,
}

export default YearSlider