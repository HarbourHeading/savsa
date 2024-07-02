import {useEffect, useState} from 'react'
import axios from 'axios'
import styles from './App.module.css'
import YearSlider from "./components/yearslider/YearSlider"
import Footer from "./components/footer/Footer.jsx"

function App() {

    const [data, setData] = useState({})
    const [loading, setLoading] = useState(true)
    const [inputValue, setInputValue] = useState(Math.round((2003 + new Date().getFullYear()) / 2))
    const [guessResult, setGuessResult] = useState('')
    const [isNewProfileLoaded, setIsNewProfileLoaded] = useState(false)


    function submitGuess() {
        let answerValue = data.timecreated ? new Date(data.timecreated * 1000).getFullYear() : null

        if (inputValue === answerValue) {
            setGuessResult('Correct! The answer was: ' + answerValue)
        }

        else {
            setGuessResult('Incorrect. The answer was: ' + answerValue)
        }

        setIsNewProfileLoaded(false)
    }

    async function fetchData() {
        await axios.get('/api/SteamProfileService/GetRandomProfile')
            .then((response) => {

                setData(response.data)
                setIsNewProfileLoaded(true)
                setGuessResult('')

            })
            .catch((error) => {

                alert('Something went wrong! Please check the console for details.')
                console.error('Something went wrong! Please send the error log to liam.e.swe@gmail.com: ', error)

            })
        setLoading(false)
    }

    useEffect(() => {
        fetchData()
    }, [])

    return (
        /* Render header and footer */
        <div className={styles.App}>
            <div className={styles.App__content}>
                {loading ? (
                    <p className={styles.App__loading}>Finding Suitable account...</p>
                ) : (
                    data && (
                        <div className={styles.profile}>
                            <div className={styles.profile__details}>
                                <br/>
                                <ul className={styles.profile__header}>
                                    <li className={styles.profile__avatar}>
                                        <img src={data.avatarmedium} alt={data.personaname}/>
                                    </li>
                                    <li className={styles.profile__level}>
                                        <p>{data.player_level}</p>
                                    </li>
                                </ul>
                                <br/>
                                <h3 className={styles.profile__recentlyPlayed_header}>Recently Played:</h3>
                                {data.recently_played?.map(game => (
                                    <div className={styles.profile__games} key={game.appid}>
                                        <img
                                            src={`https://cdn.cloudflare.steamstatic.com/steam/apps/${game.appid}/capsule_184x69.jpg`}
                                            alt={`${game.name} capsule`}/>
                                        <p> {game.name} | {Math.round(game.playtime_forever / 60)} hours</p>
                                    </div>
                                ))}
                            </div>
                            <div className={styles.profile__interactable}>
                                <YearSlider
                                    min={2003}
                                    max={new Date().getFullYear()}
                                    inputValue={inputValue}
                                    setInputValue={setInputValue}
                                    step={1}
                                />
                                <button type="button" className={styles.profile__interactable_Button}
                                        onClick={submitGuess} disabled={!isNewProfileLoaded}>Submit Guess
                                </button>
                                <button type="button" className={styles.profile__interactable_Button}
                                        onClick={fetchData}>New Profile
                                </button>
                                {guessResult && <p className={styles.profile__interactableResult}>{guessResult}</p>}
                            </div>
                        </div>
                    )
                )}
            </div>
            <Footer/>
        </div>
    )
}

export default App