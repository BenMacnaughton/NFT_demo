// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract WaterCollection is ERC721, VRFConsumerBase {

    bytes32 internal keyhash;
    uint256 public fee;
    uint256 public tokenCounter;

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    event requestedCollectible(bytes32 indexed requestId);

    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash) public
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Water Collection", "DRIP")
    {
        keyhash = _keyhash;
        fee = 0.25 * 10 ** 18;
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI)
    public returns (bytes32){
        require(tokenCounter < 100, "Max number of collectibles reached");
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address creator = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter++;
        _safeMint(creator, newItemId);
        _setTokenURI(newItemId, tokenURI);
    }

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Only approved or owner can set token URI");
        
        _setTokenURI(tokenId, tokenURI);
    }

}