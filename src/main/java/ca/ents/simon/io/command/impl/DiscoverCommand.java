package ca.ents.simon.io.command.impl;

import ca.ents.simon.io.command.AddressedSimonCommand;
import ca.ents.simon.io.command.Command;
import ca.ents.simon.io.command.RequiresResponse;
import ca.ents.simon.io.command.init.DiscoverCommandInitializer;

/**
 * Command used for discovering addresses on the network
 */
@Command(commandId = 0x09, initializer = DiscoverCommandInitializer.class)
@RequiresResponse(AckCommand.class)
public class DiscoverCommand extends AddressedSimonCommand {
    public DiscoverCommand(byte address) {
        super(address);
    }
}
