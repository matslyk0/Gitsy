import Banner from "../components/Banner/Banner.jsx";
import Footer from "../components/Footer/Footer.jsx";
import CreateReportPageButton from "../components/MainPageButtons/CreateReportPageButton.jsx";
import Introduction from "../components/Introduction/Introduction.jsx";

export default function GetStarted() {
  return (
    <>
      <Banner />
      <main>
        <Introduction />
        <CreateReportPageButton />
      </main>
      <Footer />
    </>
  );
}
