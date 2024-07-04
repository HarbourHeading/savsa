import styles from "./Footer.module.css"
import {getImageUrl} from "../../../utils.js"
import axios from "axios"
import {useState} from "react"

export const Footer = () => {

    const [steamid, setSteamid] = useState('')

    async function handleSubmitProfile(event){
        event.preventDefault()  // Prevent page refresh on form submit


        if (/[!@#$%^&*()+={}[\]:;"'<>,.?/|\\]/.test(steamid)) {  // Characters not allowed in a profile url. Will always fail to make a successful API request.
            alert('Special characters are not allowed. If you believe this is a mistake, email liam.e.swe@gmail.com')
            return
        }

        await axios.post('/api/SteamProfileService/PostSteamID', {steamid: steamid})
            .then((response) => {

                alert(response.data.message + "id: " + steamid || 'Your account has been added!')


            })
            .catch((error) => {

                if (error.response.data.error) {  // Conscious errors, Instructions in response
                    alert(error.response.data.error || "Something went wrong! Please try again.")
                }

                else if (error.response.status === 429) {  // Rate-limited
                    alert("You are sending too many requests. Please try again later.")
                }

                else {  // Unpredicted errors, more info needed
                    alert('Something went wrong! Please check the console for details.')
                    console.error('Something went wrong! Please send the error log to liam.e.swe@gmail.com: ', error)
                }

            })
    }

    return (
        <footer className={styles.footer}>
            <div className={styles.form__container}>
                <div className={styles.form__text}>
                    <p>Add your profile</p>
                </div>
                <form className={styles.form} onSubmit={handleSubmitProfile}>
                    <input
                        className={styles.form__input}
                        type="text"
                        name="steamid"
                        placeholder="Your SteamID"
                        value={steamid}
                        onChange={(e) => setSteamid(e.target.value)}
                    />
                    <button className={styles.form__button} type="submit">Submit</button>
                </form>
            </div>

            <ul className={styles.footer__links}>
                <li className={styles.footer__link}>
                    <a href="mailto:liam.e.swe@gmail.com">
                        <img src={getImageUrl("socials/email.png")} alt="Email icon"/>
                        <p>liam.e.swe@gmail.com</p>
                    </a>
                </li>

                <li className={styles.footer__link}>
                    <a target="_blank"
                       rel="noopener noreferrer"
                       aria-label="Link to my linkedin"
                       href="https://www.linkedin.com/in/Liam-e-swe">
                        <img src={getImageUrl("socials/linkedin.png")} alt="LinkedIn icon"/>
                        <p>https://linkedin.com/in/liam-e-swe</p>
                    </a>
                </li>

                <li className={styles.footer__link}>
                    <a target="_blank"
                       rel="noopener noreferrer"
                       aria-label="Link to my github"
                       href="https://www.github.com/HarbourHeading">
                        <img src={getImageUrl("socials/github.png")} alt="Github icon"/>
                        <p>https://github.com/HarbourHeading</p>
                    </a>
                </li>
            </ul>
        </footer>
    )
}

export default Footer