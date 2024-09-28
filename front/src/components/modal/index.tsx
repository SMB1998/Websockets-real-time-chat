import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  Button,
  DialogActions,
} from "@mui/material";
import styles from "./page.module.css"; // Importar los estilos si los necesitas

interface ModalProps {
  onStart: (id: string, name: string) => void;
  onClose: () => void;
}

const ModalEnter: React.FC<ModalProps> = ({ onStart, onClose }) => {
  const [userId, setUserId] = useState<string>("");
  const [userName, setUserName] = useState<string>("");

  const handleStart = () => {
    if (userId) {
      onStart(userId, userName);
    }
  };

  return (
    <Dialog open={true} onClose={onClose}>
      <DialogTitle>Bienvenido al chat</DialogTitle>
      <DialogContent>
        <TextField
          label="Id de la sala"
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          fullWidth
          margin="normal"
        />
        {/* <TextField
          label="Nombre de usuario"
          type="text"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          fullWidth
          margin="normal"
        /> */}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="secondary">
          Cerrar
        </Button>
        <Button onClick={handleStart} color="primary">
          Iniciar chat
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ModalEnter;
