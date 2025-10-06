import Banner from "../components/Banner/Banner.jsx";
import Welcome from "../components/Welcome/Welcome.jsx";
import MainPageButtons from "../components/MainPageButtons/MainPageButtons.jsx";
import Footer from "../components/Footer/Footer.jsx";

export default function Home() {
  return (
    <>
      <Banner />
      <main>
        <Welcome />
        <MainPageButtons />
      </main>
      <Footer />
    </>
  );
}
