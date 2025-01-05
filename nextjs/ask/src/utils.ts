// Generates a conversation name based on the current date and time
export const conversationName = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  // @ts-ignore
  hours = String(hours).padStart(2, '0');

  return `Conversation ${year}-${month}-${day} ${hours}:${minutes}:${seconds} ${ampm}`;
};
