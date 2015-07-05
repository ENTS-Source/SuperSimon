
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
        /// <returns>The command that represents the response</returns>
        Command Response();
    }
}
