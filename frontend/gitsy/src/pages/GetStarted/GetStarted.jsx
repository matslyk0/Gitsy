import Banner from "../../components/Banner/Banner.jsx";
import Footer from "../../components/Footer/Footer.jsx";
import Introduction from "../../components/Introduction/Introduction.jsx";

export default function GetStarted() {
  const styles = {
    justifyContent: "center",
    display: "flex",
    alignItems: "center",
    flexDirection: "column",
    border: "0px solid white" /* for debugging */,
  };

  return (
    <>
      <Banner />
      <main style={styles}>
        <Introduction />
      </main>
      <Footer />
    </>
  );
}
