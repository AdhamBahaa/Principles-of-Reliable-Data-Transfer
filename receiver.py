class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        received_checksum = packet['checksum']
    
         # Assuming there is a method to calculate checksum in your protocol
        calculated_checksum = packet['data']

        # Compare the received checksum with the calculated checksum
        return received_checksum != ord(calculated_checksum)
    
    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        received_sequence = rcv_pkt['sequence_number']
    
         # Compare the received sequence number with the expected sequence number
        return received_sequence == exp_seq


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """

         # Check if the packet is not corrupted and has the expected sequence number
        if not self.is_corrupted(rcv_pkt) and self.is_expected_seq(rcv_pkt, self.sequence):
            # Deliver the data to the process in the application layer
            ReceiverProcess.deliver_data(rcv_pkt['data'])
            print("snd")
            # Create and send an acknowledgment (ACK) packet
            reply_pkt = self.make_reply_pkt(self.sequence, ord(self.sequence))
            self.sequence = '1' if self.sequence == '0' else '0'  # Switch between 0 and 1 for alternating bit

        else:
            if(self.sequence == '0'):
                reply_pkt = self.make_reply_pkt('1', ord('1'))
            else:
                reply_pkt = self.make_reply_pkt('0', ord('0'))
                

        print("\033[92mReceiver is expecting: \033[0m" + self.sequence)
        print("\033[92mReceiever replied: \033[0m", reply_pkt)
        return reply_pkt

        # If the packet is corrupted or has an unexpected sequence number, return None