import { Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import Signup from "./pages/signup";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<Signup />} />
    </Routes>
  );
}

export default App;