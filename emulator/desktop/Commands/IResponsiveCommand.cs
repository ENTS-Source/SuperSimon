
namespace SuperSimonEmulator.Commands
{
    /// <summary>
    /// Indicates that this command generates a response when executed
    /// </summary>
    public interface IResponsiveCommand
    {
        /// <summary>
        /// Generates a response for this command
        /// </summary>
        /// <param name="pad">The game pad that the command was executed on, if any</param>
        /// <returns>The command that represents the response</returns>
        Command Response(GamePad pad);
    }
}
