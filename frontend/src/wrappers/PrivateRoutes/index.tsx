import Loading from "@/components/Loading";
import PrivateLayout from "@/components/PrivateLayout";
import { useAuth } from "@/contexts/AuthContext";
import { Navigate, Outlet } from "react-router-dom";

const PrivateRoutes = () => {
  const { isAuthed, isLoading } = useAuth();
  if (isLoading) {
    return <Loading />;
  }
  if (!isAuthed) {
    return <Navigate to="/login" />;
  }
  return <PrivateLayout><Outlet /></PrivateLayout>;
};

export default PrivateRoutes;