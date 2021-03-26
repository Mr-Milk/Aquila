import Head from "next/head";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import Header from "../components/Header";
import Footer from "../components/Footer";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#26a69a",
      light: "#64d8cb",
      dark: "#00766c",
    },
  },
});

export default function layout({ children }) {
  return (
    <ThemeProvider theme={theme}>
      <Head>
        <title>Baize</title>
        <link rel="icon" href="/favicon.ico" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
        />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/icon?family=Material+Icons"
        />
      </Head>
      <main>
        <Header />
        <Container maxWidth="lg">{children}</Container>
      </main>
      <Footer />
    </ThemeProvider>
  );
}
