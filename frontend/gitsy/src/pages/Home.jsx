import Banner from "../components/Banner/Banner.jsx";
import Welcome from "../components/Welcome/Welcome.jsx";
import MainButtons from "../components/MainButtons/MainButtons.jsx";
import Footer from "../components/Footer/Footer.jsx";

export default function Home() {
  return (
    <>
      <Banner />
      <main>
        <Welcome />
        <MainButtons />
      </main>
      <Footer />
    </>
  );
}
