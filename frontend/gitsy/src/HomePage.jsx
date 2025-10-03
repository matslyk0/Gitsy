import Banner from "./Banner/Banner.jsx";
import Welcome from "./Welcome/Welcome.jsx";
import MainButtons from "./MainButtons/MainButtons.jsx";
import Footer from "./Footer/Footer.jsx";

export default function HomePage() {
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
