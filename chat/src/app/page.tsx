"use client";
import React, { useState, useEffect } from "react";
import styles from "./page.module.css"; // Asegúrate de que este archivo exista en el mismo directorio
import "@fortawesome/fontawesome-free/css/all.min.css"; // Importar Font Awesome
import ModalEnter from "@/components/modal";
import Snackbar from "@mui/material/Snackbar";
import MuiAlert, { AlertProps } from "@mui/material/Alert";

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
  props,
  ref
) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

// Componente de chat con WebSocket
interface WebSocketChatProps {
  roomId: string;
  userName: string;
}

const WebSocketChat: React.FC<WebSocketChatProps> = ({ roomId, userName }) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [message, setMessage] = useState<string>("");
  const [badRoom, setBadRoom] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [messages, setMessages] = useState<{ user: number; content: string }[]>(
    []
  );
  const [openSnackbar, setOpenSnackbar] = useState(false);

  useEffect(() => {
    setLoading(true);
    const ws = new WebSocket(`ws://34.69.94.81:8000/ws/chat/${roomId}/`);
    ws.onopen = () => {
      console.log(`Conectado a la sala: ${roomId}`);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setBadRoom(data.type === "bad_room");
      setMessages(data.messages);

      if (data.type === "bad_room") {
        setOpenSnackbar(true); // Abrir Snackbar si la sala no existe
      }
      setLoading(false);
    };

    ws.onclose = () => {
      console.log("Desconectado del WebSocket");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [roomId]);

  const sendMessage = () => {
    if (socket && message.trim() !== "") {
      socket.send(
        JSON.stringify({
          room: 1, // Quemado temporalmente
          user: 1,
          content: message,
        })
      );
      setMessage(""); // Limpiar el campo de texto después de enviar
    }
  };

  // Manejar el evento de la tecla Enter
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <div className={styles.card}>
      <div style={{ color: "black" }}>{`${roomId}`}</div>
      <div className={styles.chatContainer}>
        {loading && (
          <Alert
            onClose={handleCloseSnackbar}
            severity="info"
            sx={{ width: "100%" }}
          >
            Cargando mensajes...
          </Alert>
        )}

        <div className={styles.messages}>
          <ul>
            {messages?.map((msg, index) => (
              <li key={index} className={styles.messageItem}>
                <div className={styles.messageBubble}>
                  <div className={styles.messageContent}>
                    <div style={{ display: "flex", flexDirection: "row" }}>
                      <div className={styles.userIcon}>
                        <i className="fas fa-user-circle"></i>
                      </div>
                      <strong>{`Usuario ${msg.user}`}:</strong>{" "}
                    </div>
                    {msg.content}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <div className={styles.inputContainer}>
          <input
            type="text"
            className={styles.inputField}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Escribe un mensaje..."
            style={{ color: "black" }}
          />
          <button className={styles.sendButton} onClick={sendMessage}>
            Enviar
          </button>
        </div>
      </div>

      {/* Snackbar para mostrar mensaje de error */}
      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity="error"
          sx={{ width: "100%" }}
        >
          No existe este tablero, puedes crearlo ingresando un mensaje.
        </Alert>
      </Snackbar>
    </div>
  );
};

const Home: React.FC = () => {
  const [roomId, setRoomId] = useState<string | null>(null);
  const [userName, setUserName] = useState<string>("");
  const [modalVisible, setModalVisible] = useState<boolean>(true); // Controlar visibilidad del modal

  useEffect(() => {
    // Verificar si hay un query param 'salaId' en la URL
    const queryParams = new URLSearchParams(window.location.search);
    const salaId = queryParams.get("salaId");

    if (salaId) {
      setRoomId(salaId);
      setModalVisible(false); // Cerrar el modal
    } else {
      setModalVisible(true); // Mostrar el modal si no hay salaId
    }
  }, []);

  const handleStartChat = (id: string, name: string) => {
    setRoomId(id);
    setUserName(name);
    setModalVisible(false);

    // Añadir el query param 'salaId' a la URL sin recargar la página
    if (typeof window !== "undefined") {
      const newUrl = `${window.location.pathname}?salaId=${id}`;
      window.history.pushState({}, "", newUrl); // Cambiar la URL sin recargar la página
    }
  };

  const handleCloseModal = () => {
    setModalVisible(false); // Ocultar modal sin iniciar chat
  };

  return (
    <div className={styles.homeContainer} key={roomId}>
      {modalVisible && (
        <ModalEnter onStart={handleStartChat} onClose={handleCloseModal} />
      )}
      {roomId !== null && !modalVisible && (
        <WebSocketChat roomId={roomId} userName={userName} />
      )}
    </div>
  );
};

export default Home;
