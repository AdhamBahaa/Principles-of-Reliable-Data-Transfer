class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer
    
class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
        It initializes the RDT sender sequence number to '0' and the network layer services
        The network layer service provides the method udt_send(send_pkt)
        """
        
        self.sequence = '0'
        self.net_srv = net_srv

    @staticmethod
    def get_checksum(data):
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example, data = 'A'
        :return: the ASCII code of the character, for example, ASCII('A') = 65
        """
        checksum = ord(data) 
        return checksum

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as a python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    @staticmethod
    def is_corrupted(reply):
        #Check if the received reply from the receiver is corrupted or not.
        #Recalculate the checksum based on the received data
        calculated_checksum = RDTSender.get_checksum(reply['ack'])

        # Compare the calculated checksum with the received checksum
        return reply['checksum'] != calculated_checksum



    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from the receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply matches the expected sequence number otherwise False
        """
        ack_sequence = reply['ack']

        # For an alternating bit protocol, only accept the expected sequence number
        return ack_sequence == exp_seq
 
    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender wants to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):
        #Implement the RDT v2.2 for the sender.
    
        # Track the index of the current data being sent
        current_index = 0

        while current_index < len(process_buffer):
            data = process_buffer[current_index]
            checksum = RDTSender.get_checksum(data)
            pkt = RDTSender.make_pkt(self.sequence, data, checksum)
            copy = RDTSender.clone_packet(pkt)
            
        # Send the packet and wait for acknowledgment
            reply = self.net_srv.udt_send(pkt)
            while True:
                print("\033[96mSender received: \033[0m", reply)
                print("\033[96mSender is expecting seq_num: \033[0m", self.sequence)
                print("\033[96mSender is sending: \033[0m", pkt)
                if not RDTSender.is_corrupted(reply) and  RDTSender.is_expected_seq(reply, self.sequence):
                    # Acknowledgment received, move to the next sequence number
                    self.sequence = '0' if self.sequence == '1' else '1'
                    current_index += 1
                    break
                else:
                    pkt = RDTSender.clone_packet(copy)
                    # Wrong acknowledgment, move on to the next packet
                    reply = self.net_srv.udt_send(pkt)
                
            
        print('Sender Done!')

  


        
